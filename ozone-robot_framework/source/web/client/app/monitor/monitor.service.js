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
  .service('monitor', function ($http) {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var uri = '/api/monitor';
    this.getStatus = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/health',configureData).then(successCallback,errorCallback)
    };

    this.getVersion = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/version',configureData).then(successCallback,errorCallback)
    };

    this.getLicense = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/license',configureData).then(successCallback,errorCallback)
    };

    this.getSSLCertificate = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/ssl_certs',configureData).then(successCallback,errorCallback)
    };


  });
