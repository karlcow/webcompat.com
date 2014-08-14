#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Flask Blueprint for our "API" module, which is used to proxy API calls
back to GitHub'''

import json
from flask import abort, Blueprint, g, request, session
from flask.ext.github import GitHubError
from webcompat import github, app
from ..issues import (proxy_request, filter_needs_diagnosis,
                      filter_contactready, REPO_URI)
from ..helpers import get_user_info

api = Blueprint('api', __name__, url_prefix='/api')
JSON_MIME = 'application/json'


def ensure_xhr(fn):
    '''Decorator to restrict requests to XHR.'''
    def check(*args, **kwargs):
        if request.is_xhr and request.headers.get('accept') == JSON_MIME:
            return fn(*args, **kwargs)
        else:
            abort(406)
    return check


@ensure_xhr
@api.route('/issues')
def proxy_issues():
    '''API endpoint to list all issues from GitHub.'''
    if g.user:
        issues = github.get('repos/{0}'.format(REPO_URI))
    else:
        issues = proxy_request('get')
    if request.args.get('needsdiagnosis') == '1':
        return json.dumps(filter_needs_diagnosis(issues))
    elif request.args.get('contactready') == '1':
        return json.dumps(filter_contactready(issues))
    else:
        return json.dumps(issues)


@ensure_xhr
@api.route('/issues/<int:number>')
def proxy_issue(number):
    '''XHR endpoint to get issue data from GitHub, either as an authed
    user, or as one of our proxy bots.'''
    if g.user:
        issue = github.get('repos/{0}/{1}'.format(
            app.config['ISSUES_REPO_URI'], number))
    else:
        issue = proxy_request('get', '/{0}'.format(number))
    return json.dumps(issue)


@ensure_xhr
@api.route('/issues/<int:number>/edit', methods=['PATCH'])
def edit_issue(number):
    '''XHR endpoint to push back edits to GitHub for a single issue.
    Note: this is always proxied to allow any logged in user to be able to
    edit issues.'''
    edit = proxy_request('patch', '/{0}'.format(number), data=request.data)
    return json.dumps(edit)


@ensure_xhr
@api.route('/issues/mine')
def user_issues():
    '''API endpoint to return issues filed by the logged in user.'''
    get_user_info()
    issues = github.get('repos/{0}?creator={1}&state=all'.format(
        REPO_URI, session['username']))
    return json.dumps(issues)


@ensure_xhr
@api.route('/issues/contactready')
def get_contactready():
    '''Return all issues with a "contactready" label.'''
    if g.user:
        uri = 'repos/{0}?labels=contactready'.format(REPO_URI)
        issues = github.get(uri)
    else:
        issues = proxy_request('get', '?labels=contactready')
    return json.dumps(issues)


@api.route('/issues/<int:number>/comments', methods=['GET', 'POST'])
def proxy_comments(number):
    '''XHR endpoint to get issues comments from GitHub, either as an authed
    user, or as one of our proxy bots.'''
    if request.method == 'POST':
        try:
            comment_data = json.loads(request.data)
            body = {"body": comment_data['rawBody']}
            github.post('repos/{0}/{1}/comments'.format(
                REPO_URI, number), body)
            return ':)'
        except GitHubError as e:
            print('GitHubError: ', e.response.status_code)
            return (':(', e.response.status_code)
    elif request.is_xhr and request.headers.get('accept') == JSON_MIME:
        if g.user:
            comments = github.get('repos/{0}/{1}/comments'.format(
                app.config['ISSUES_REPO_URI'], number))
        else:
            comments = proxy_request('get', '/{0}/comments'.format(number))
        return json.dumps(comments)
    else:
        abort(406)


@ensure_xhr
@api.route('/issues/<int:number>/labels', methods=['POST'])
def modify_labels(number):
    '''XHR endpoint to modify issue labels. Sending in an empty array removes
    them all as well. This method is always proxied because non-repo collabs
    can't normally edit labels for an issue.'''
    try:
        labels = proxy_request('put', '/{0}/labels'.format(number),
                               data=request.data)
        return json.dumps(labels)
    except GitHubError as e:
        print('GitHubError: ', e.response.status_code)
        return (':(', e.response.status_code)


@ensure_xhr
@api.route('/issues/labels')
def get_repo_labels():
    '''XHR endpoint to get all possible labels in a repo.'''
    # Chop off /issues. Someone feel free to refactor the ISSUES_REPO_URI.
    labels_uri = app.config['ISSUES_REPO_URI'][:-7]
    if g.user:
        labels = github.get('repos/{0}/labels'.format(labels_uri))
    else:
        labels = proxy_request('get', '/labels', uri=labels_uri)
    return json.dumps(labels)