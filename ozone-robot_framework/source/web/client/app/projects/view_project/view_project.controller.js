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
(function(){

class ViewProjectComponent {
  constructor($scope, $stateParams, projects, $location) {
    $scope.selected = [];

    $scope.projects = projects;
    projects.refreshDefaultConfigData();

    projects.getProject($stateParams.id,function(response){
      $scope.project = response.data;
    });

    $scope.formStatus = 'pending';


    $scope.buttontheme = 'default';

    $scope.submitForm = function() {
      $scope.buttonicon = 'refresh';

      projects.update($scope.project,
        function (successResponse) {
          $scope.buttonicon = 'check';
          $scope.buttontheme = 'green';
          $scope.formStatus = 'success';
          setTimeout(function () {
            $location.path('/projects');
            $scope.$apply();
          }, 1000);
        },
        function (errorResponse) {
          $scope.buttonicon = 'error';
          $scope.buttontheme = 'red';
          $scope.formStatus = 'Fail';
          $scope.errmsg = errorResponse.data;
        }
      );

    };

    $scope.cancelForm = function(){
      $location.path('/projects');
    };


    $scope.update_playbook_state = 'default';
    $scope.updatePlaybook = function(){

      $scope.update_playbook_state = 'RUNNING';
      projects.updateAnsiblePlaybookFiles($scope.project, function(response){
        $scope.update_playbook_state = 'SUCCESS';
      }, function(response){
        $scope.update_playbook_state = 'FAIL';
        $scope.update_fail_message = response.data;
      })

    }

  }
}

angular.module('ehcOzoneApp')
  .component('viewProject', {
    templateUrl: 'app/projects/view_project/view_project.html',
    controller: ViewProjectComponent
  });

})();
