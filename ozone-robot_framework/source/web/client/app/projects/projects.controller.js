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

class ProjectsComponent {
  constructor($scope, projects, $q, $rootScope, $mdDialog, toasts) {
    $scope.query = {
      order: 'name',
      limit: 5,
      page: 1
    };
    $scope.selected = [];

    /**
     * Get Projects
     */
    $scope.getProjects = function(){
      projects.getProjects(
        function(successResponse){
          $scope.projects = successResponse.data;
          $scope.selected = [];
        },
        function(errResponse){
          $scope.errmsg = errResponse.data;
        });
    };

    /**
     * Show Confirmation message before delete
     * @param ev
     */
    $scope.showConfirm = function(ev) {
      // Appending dialog to document.body to cover sidenav in docs app
      var confirm = $mdDialog.confirm()
        .title('Confirm')
        .textContent('Are you sure you want to delete the selected project(s)?')
        .ariaLabel('Delete')
        .targetEvent(ev)
        .ok('Yes')
        .cancel('No');
      $mdDialog.show(confirm).then(function() {
        $scope.deleteProjects()
      }, function() {

      });
    };

    /**
     * Delete Projects
     */
    $scope.deleteProjects = function(){

        $q.all($scope.selected.map(function(selectedProject){
          return projects.deleteProject(selectedProject);
        })).then(function(results){

          results.forEach(function (val, i) {

          });
          $rootScope.$emit('notify-refresh-projects');
          $scope.getProjects();
        },  function(errResponse){
          console.log(errResponse.data || errResponse);
          toasts.showError(errResponse.data || errResponse,"Error", "red");
        });

    };

    $scope.getProjects();
    projects.refresh();

  }
}

angular.module('ehcOzoneApp')
  .component('projects', {
    templateUrl: 'app/projects/projects.html',
    controller: ProjectsComponent
  });

})();
