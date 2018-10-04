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
  .filter('customFilter', function () {
    return function (input, search) {
      if (!input) return input;
      if (!search) return input;
      var expected = ('' + search).toLowerCase();
      var result = {};
      angular.forEach(input, function(value, key) {
        var actual = ('' + value).toLowerCase();
        var actual_key = ('' + key).toLowerCase();
        if (actual.indexOf(expected) !== -1 || actual_key.indexOf(expected) !== -1) {
          result[key] = value;
        }
      });
      return result;
    };
  });
