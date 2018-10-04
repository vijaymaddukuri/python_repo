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
  .service('configure', function ($http, toasts ) {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var uri = '/api/configure';
    this.create = function(configureData,successCallback,errorCallback){
      $http.post(uri,configureData).then(successCallback,errorCallback)
    };

    this.generateCerts = function(configureData,successCallback,errorCallback){
      $http.post(uri + '/generateCerts',configureData).then(successCallback,errorCallback)
    };

    this.get = function(projectid,type,successCallback,errorCallback){
      $http.get(uri,{params:{refid:projectid+"_"+type}}).then(successCallback,errorCallback);
    };

    this.show = function(configureId,successCallback,errorCallback){
      $http.get(uri + '/' + configureId).then(successCallback,errorCallback);
    };

    this.getLogs = function(configureData,successCallback,errorCallback){
      $http.get(uri+'/'+configureData._id+'/logs').then(successCallback,errorCallback);
    };

    this.getAnsibleTasksList = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/ansible/listtasks', configureData).then(successCallback,errorCallback);
    };

    this.getAnsiblePlaybooksList = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/ansible/listplaybooks', configureData).then(successCallback,errorCallback);
    };

    this.getLastGoodConfigurations = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/ansible/last_good_configurations', configureData).then(successCallback,errorCallback);
    };

    this.executeAnsiblePlayBook = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/ansible/execute', configureData).then(successCallback,errorCallback);
    };

    this.stopAnsiblePlayBookExecution = function(configureData,successCallback,errorCallback){
      $http.post(uri+'/ansible/stop', configureData).then(successCallback,errorCallback);
    };

    this.showfehcPythonLogs = function(){
      toasts.showLogs('Fetching Logs....', 'Agent Logs', 'blue', 'bottom right');
    }

  });
