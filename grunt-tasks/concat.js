/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

module.exports = function(grunt) {
  grunt.config("concat", {
    options: {
      banner: "<%= banner %>",
      stripBanners: false
    },
    dist: {
      src: [
        "<%= jsPath %>/vendor/jquery-1.11.2.min.js",
        "<%= jsPath %>/vendor/lodash.custom.min.js",
        "<%= jsPath %>/vendor/backbone-min.js",
        "<%= jsPath %>/vendor/moment-min.js",
        "<%= jsPath %>/vendor/prism.js",
        "<%= jsPath %>/vendor/markdown-it.js",
        "<%= jsPath %>/vendor/markdown-it-emoji-1.0.0.js",
        "<%= jsPath %>/vendor/markdown-it-sanitizer-0.4.1.js",
        "<%= jsPath %>/vendor/mousetrap-min.js",
        "<%= jsPath %>/vendor/backbone.mousetrap.js",
        "<%= jsPath %>/lib/flash-message.js",
        "<%= jsPath %>/lib/homepage.js",
        "<%= jsPath %>/lib/bugform.js",
        "<%= jsDistPath %>/templates.js"
      ],
      dest: "<%= jsDistPath %>/<%= pkg.name %>.js"
    },
    diagnose: {
      src: [
        "<%= jsPath %>/lib/models/label-list.js",
        "<%= jsPath %>/lib/models/issue.js",
        "<%= jsPath %>/lib/diagnose.js"
      ],
      dest: "<%= jsDistPath %>/diagnose.js"
    },
    issues: {
      src: [
        "<%= jsPath %>/lib/mixins/extend-md-sanitizer.js",
        "<%= jsPath %>/lib/models/label-list.js",
        "<%= jsPath %>/lib/editor.js",
        "<%= jsPath %>/lib/labels.js",
        "<%= jsPath %>/lib/models/milestones.js",
        "<%= jsPath %>/lib/milestones.js",
        "<%= jsPath %>/lib/models/issue.js",
        "<%= jsPath %>/lib/models/comment.js",
        "<%= jsPath %>/lib/comments.js",
        "<%= jsPath %>/lib/issues.js"
      ],
      dest: "<%= jsDistPath %>/issues.js"
    },
    issueList: {
      src: [
        "<%= jsPath %>/lib/models/label-list.js",
        "<%= jsPath %>/lib/models/issue.js",
        "<%= jsPath %>/lib/mixins/pagination.js",
        "<%= jsPath %>/lib/mixins/extend-md-sanitizer.js",
        "<%= jsPath %>/lib/issue-list.js"
      ],
      dest: "<%= jsDistPath %>/issue-list.js"
    },
    userActivity: {
      src: [
        "<%= jsPath %>/lib/models/label-list.js",
        "<%= jsPath %>/lib/models/issue.js",
        "<%= jsPath %>/lib/mixins/pagination.js",
        "<%= jsPath %>/lib/user-activity.js"
      ],
      dest: "<%= jsDistPath %>/user-activity.js"
    }
  });
};
