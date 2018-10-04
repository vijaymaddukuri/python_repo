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
  .service('upgrade', function ($http) {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var uri = '/api/upgrade';

    this.create = function(successCallback,errorCallback){
      $http.post(uri).then(successCallback,errorCallback)
    };

    this.get = function(successCallback,errorCallback){
      $http.get(uri).then(successCallback,errorCallback);
    };

    this.getLogs = function(deployObject,successCallback,errorCallback){
      $http.get(uri+'/logs/'+deployObject._id).then(successCallback,errorCallback);
    };

    this.checkUpdates = function(successCallback,errorCallback){
      $http.get(uri + '/check_updates').then(successCallback,errorCallback)
    }
  });
