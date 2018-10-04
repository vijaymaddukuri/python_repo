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

class ConfigureComponent {
  constructor($scope,projects,configure,messageus,tile,log,Auth,toasts,$mdDialog, $interval) {

    var baseTile = tile.getBaseTile();
    $scope.dataLoaded = false;
    //$scope.hasConfigureRole = Auth.hasRole('configure');
    $scope.hasConfigureRole = true;
    $scope.selectedComponents = [];

    $scope.additional_options = {
      advanced_settings: false
    };

    $scope.getLogsService = configure.getLogs;

    $scope.showEmailUs = function(ev){
      messageus.showInputDialog(ev,"Count me In!","Tell us about yourself.","green");
    };

    $scope.workflows = [];
    $scope.refreshLog = {value: false};
    $scope.result = null;

    configure.showfehcPythonLogs();

    /**
     * Get Configuration information for a workflow
     * @param workflow
     */
    $scope.getconfigureInfo = function(workflow){
      workflow.loading = true;
      configure.get(projects.selectedProject._id, workflow.objectType, function(successResponse) {
          workflow.loading = false;
          workflow.configureObject = successResponse.data[successResponse.data.length - 1];
          workflow.jobObject = workflow.configureObject;
          workflow.jobObjects = successResponse.data;
          workflow.buttonText = 'Configure';

          if(workflow.configureObject){
            log.refreshLogs(workflow,$scope,configure.getLogs);
          }
        },
        function(errorResponse){
          workflow.loading = false;
          workflow.buttonText = 'Configure';
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
        });
    };

    $scope.state = {
      value: 'default'
    };

    /**
     * When a project is changed
     */
    $scope.selectedProjectChanged = function(){

      //$scope.hasConfigureRole = Auth.hasRole('configure');
      $scope.hasConfigureRole = true;

      console.log("$scope.hasConfigureRole=" + $scope.hasConfigureRole);

      if(!$scope.hasConfigureRole)return;
      $scope.dataLoaded = true;
      $scope.workflows = [];

      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.import_data && projects.selectedProject.components.import_data.hosts){

        getJobsData();
        if($scope.timer)$interval.cancel( $scope.timer );

        $scope.timer = $interval(function(){
          getJobsData();
        },10000);

        if($scope){
          $scope.$on(
            "$destroy",
            function( event ) {
              $interval.cancel( $scope.timer );
            }
          );
        }

      }

    };


    /**
     * Get Jobs Data
     */
    var getJobsData = function(){

      configure.getLastGoodConfigurations({project: projects.selectedProject},
        function(response){
          console.log(response.data);
          $scope.lastGoodConfigurations = response.data;
        }, function(response){
          console.error(response.data)
        });

      $scope.gettingAnsiblePlaybooks = true;

      configure.getAnsiblePlaybooksList({project: projects.selectedProject}, function(response){
        $scope.gettingAnsiblePlaybooks = false;
        $scope.configureCandidates = response.data;
        angular.forEach($scope.configureCandidates,function(configureCandidate) {

          var tempWorkflow = angular.copy(baseTile);
          tempWorkflow.title = configureCandidate.split(".")[0].toUpperCase();
          tempWorkflow.objectType = configureCandidate.split(".")[0];
          tempWorkflow.state = 'default';

          var workflowFound = false;
          angular.forEach($scope.workflows, workflow => {
              if(workflow.title === tempWorkflow.title){
                  $scope.getconfigureInfo(workflow);
                workflowFound = true;
              }
          });

          if(!workflowFound){
            $scope.workflows.push(tempWorkflow);
            $scope.getconfigureInfo(tempWorkflow);
          }

        });



      }, function(response){
        $scope.gettingAnsiblePlaybooks = false;
        toasts.showError(errorResponse.data, 'Error', 'red');
      })
    };

    /**
     * Show Last Good Configurations
     * @param ev
     */
    $scope.showLastGoodConfigurations  = function(ev){

      $mdDialog.show({
        controller: 'LastGoodConfigurationCtrl',
        //component: 'lastGoodConfigurations',
        templateUrl: '/app/configure/last_good_configurations/last_good_configurations.html',
        parent: angular.element(document.body),
        targetEvent: ev,
        clickOutsideToClose: true,
      }).then(function(data) {
          // NO Action when dialogue closes
      }, function() {
        // NO Action when dialogue closes
      });

    };


    $scope.progressType='blue';

    $scope.getStyle = tile.getStyle;

    projects.subscribeCustom($scope,$scope.selectedProjectChanged);

    if(!$scope.dataLoaded){
      $scope.selectedProjectChanged()
    }

    //projects.refresh();

  }
}

angular.module('ehcOzoneApp')
  .component('configure', {
    templateUrl: 'app/configure/configure.html',
    controller: ConfigureComponent
  });

})();
