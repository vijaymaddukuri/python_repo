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
  .service('snapshot', function ($http) {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var uri = '/api/snapshots';
    this.create = function(configureData,successCallback,errorCallback){
      $http.post(uri,configureData).then(successCallback,errorCallback)
    };

    this.get = function(projectid,type,successCallback,errorCallback){
      $http.get(uri,{params:{refid:projectid+"_"+type}}).then(successCallback,errorCallback);
    };

    this.listSnapshots = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/list',configureData).then(successCallback,errorCallback);
    };

    this.getLogs = function(configureData,successCallback,errorCallback){
      $http.get(uri+'/'+configureData._id+'/logs').then(successCallback,errorCallback);
    };
  });
