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
  .service('user', function ($http) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    var uri = 'api/users';

    this.getDefaultEHCUsers = function(successCallback,errorCallback){
      $http.get(uri + '/ehcdefaultusers').then(successCallback,errorCallback);
    };

    this.getUserByType = function(type,selectedProject){
      if(selectedProject && selectedProject.components && selectedProject.components.users && selectedProject.components.users.userList){
        var found_user = null;
        angular.forEach(selectedProject.components.users.userList,function(user){
          if(user.Name === type){
            found_user = user
          }
        });
        return found_user
      }
    };

  });
