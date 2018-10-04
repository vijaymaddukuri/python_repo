/*
 * Copyright (c) 2016 DELL EMC Corporation
 * All Rights Reserved
 *
 * This software contains the intellectual property of DELL EMC Corporation
 * or is licensed to DELL EMC Corporation from third parties.  Use of this
 * software and the intellectual property contained therein is expressly
 * limited to the terms and conditions of the License Agreement under which
 * it is provided by or on behalf of DELL  EMC.
 */


'use strict';

angular.module('ehcOzoneApp')
  .service('mdescape', function () {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var replacements = [
      [ /\*/g, '\\*' ],
      [ /#/g, '\\#' ],
      [ /\//g, '\\/' ],
      [ /\(/g, '\\(' ],
      [ /\)/g, '\\)' ],
      [ /\[/g, '\\[' ],
      [ /\]/g, '\\]' ],
      [ /\</g, '&lt;' ],
      [ /\>/g, '&gt;' ],
      [ /_/g, '\\_' ] ];

    this.markdown_escape = function(string) {
      return replacements.reduce(
        function(string, replacement) {
          return string.replace(replacement[0], replacement[1])
        },
        string)
    };
  });
