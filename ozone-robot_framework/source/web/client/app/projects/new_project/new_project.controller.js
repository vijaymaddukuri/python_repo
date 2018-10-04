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

class NewProjectComponent {
  constructor($scope,$location,projects,$rootScope) {

    $scope.project = {capacityType:'GB'};
    $scope.projects = projects;

    $scope.formStatus = 'pending';

    $scope.selectedProject = projects.selectedProject;
    $rootScope.$on('notifying-project-change', function(){
      $scope.selectedProject = projects.selectedProject;

    });

    $scope.buttontheme = 'default';

    $scope.cancelForm = function(){
      $location.path('/projects');
    };

    $scope.submitForm = function() {


      if(!$scope.project.type){
        $scope.errmsg = "Please select a Project Type";
        return
      }

      if(!$scope.project.name){
        $scope.errmsg = "Please enter a Project Name";
        return
      }

      $scope.buttonicon = 'refresh';

      if($scope.copyComponents){
        $scope.project.components = angular.copy(projects.selectedProject.components);
      }

      projects.createProject($scope.project,
        function(successResponse){

          localStorage.selectedProjectID = successResponse.data._id;
          console.log("Setting selected project to " + successResponse.data._id);


          $scope.buttonicon = 'check';
          $scope.buttontheme = 'green';
          $scope.formStatus = 'success';
          $rootScope.$emit('notify-refresh-projects');

          setTimeout(function () {
            $location.path('/projects');
            $scope.$apply();
          }, 1000);
        },
        function(errorResponse){
          console.log('Createproject Error =' + errorResponse.data);
          $scope.buttonicon = 'error';
          $scope.buttontheme = 'red';
          $scope.formStatus = 'Fail';
          $scope.errmsg = errorResponse.data;
        }
      );

    }

    projects.refreshDefaultConfigData();

  }
}

angular.module('ehcOzoneApp')
  .component('newProject', {
    templateUrl: 'app/projects/new_project/new_project.html',
    controller: NewProjectComponent
  });

})();
