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

(function() {

function authInterceptor($rootScope, $q, $cookies, $injector, Util) {
  var state;
  return {
    // Add authorization token to headers
    request(config) {
      config.headers = config.headers || {};
      if ($cookies.get('token') && Util.isSameOrigin(config.url)) {
        config.headers.Authorization = 'Bearer ' + $cookies.get('token');
      }
      return config;
    },

    // Intercept 401s and redirect you to login
    responseError(response) {
      if (response.status === 401) {
        (state || (state = $injector.get('$state'))).go('login');
        // remove any stale tokens
        $cookies.remove('token');
      }
      return $q.reject(response);
    }
  };
}

angular.module('ehcOzoneApp.auth')
  .factory('authInterceptor', authInterceptor);

})();
