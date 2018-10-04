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
  .controller('LastGoodConfigurationCtrl', function ($scope,$mdDialog, ansible, projects, $location) {

    $scope.selectedConfigurations = [];

    ansible.getLastGoodConfigurations({project: projects.selectedProject},
      function(response){
        console.log(response.data);
        $scope.lastGoodConfigurations = response.data;

      }, function(response){
        console.error(response.data)
      });

    $scope.toDate = function(stringDate){

      if(!stringDate)return null;

      var d = new Date(stringDate);

      if (d == "Invalid Date"){
        return stringDate
      }else{
        return d
      }

    };

    /**
     * Close dialogue
     */
    $scope.cancel = function() {
      $mdDialog.cancel();
    };

    /**
     * Restore Last Good Configuration
     */
    $scope.restoreLastGoodCondition = function(configuration){
      $mdDialog.cancel();
    }

  });
