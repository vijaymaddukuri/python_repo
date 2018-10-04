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
  .service('kue', function ($http) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    var uri = '/api/kue';

    this.killJob = function(jobId, configureId, successCallback, errorCallback){
      $http.post(uri + '/' + jobId+'/kill', {configureId:configureId}).then(successCallback, errorCallback);
    }

  });
