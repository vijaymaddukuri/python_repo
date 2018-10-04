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
  .service('logExplorer', function ($http, projects) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    var uri = '/api/logs/';
    var vRALogsuri = '/api/logs/vra';

    /**
     * Get Files List
     * @param successCallback
     * @param errorCallback
     */
    this.getFilesList = function(successCallback, errorCallback){
      $http.get(uri).then(successCallback, errorCallback);
    };

    /**
     * Get File
     * @param filePath
     * @param successCallback
     * @param errorCallback
     */
    this.getFile = function(filePath, successCallback, errorCallback){
      $http.post(uri,{filePath:filePath}).then(successCallback, errorCallback);
    };

    /**
     * Get Logs
     * @param type
     * @param lines
     * @param successCallback
     * @param errorCallback
     */
    this.getLogs = function(type, lines, successCallback, errorCallback){
      if(type == 'vraLogs'){
        $http.get(vRALogsuri + '/' + projects.selectedProject._id).then(successCallback, errorCallback);
      }else{
        $http.get(uri + 'service/' + type + '/' + lines).then(successCallback, errorCallback);
      }
    };


  });
