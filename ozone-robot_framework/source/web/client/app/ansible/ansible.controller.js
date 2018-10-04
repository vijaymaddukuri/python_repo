'use strict';
(function(){

class AnsibleComponent {
  constructor($scope,projects,ansible,messageus,tile,log,Auth,toasts,$mdDialog, $interval) {
    var baseTile = tile.getBaseTile();
    $scope.dataLoaded = false;
    //$scope.hasConfigureRole = Auth.hasRole('configure');
    $scope.hasConfigureRole = true;
      $scope.selectedComponents = [];

    $scope.additional_options = {
      advanced_settings: false
    };

    $scope.isSuperAdmin = Auth.hasRole('superadmin');

    $scope.getLogsService = ansible.getLogs;

    $scope.showEmailUs = function(ev){
      messageus.showInputDialog(ev,"Count me In!","Tell us about yourself.","green");
    };

    $scope.workflows = [];
    $scope.refreshLog = {value: false};
    $scope.result = null;

    ansible.showAgentLogsPopup();

    /**
     * Get Configuration information for a workflow
     * @param workflow
     */
    $scope.getansibleInfo = function(workflow){
      workflow.loading = true;
      ansible.get(projects.selectedProject._id, workflow.objectType, function(successResponse) {
          workflow.loading = false;
          workflow.jobObject = successResponse.data[successResponse.data.length - 1];
          workflow.jobObjects = successResponse.data;
          workflow.buttonText = 'Configure';

          // if(workflow.jobObject){
          //   log.refreshLogs(workflow,$scope,ansible.getLogs);
          // }
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
          console.log("Interval Get Jobs Data " + $scope.timer);
          getJobsData();
        },25000);

        if($scope){
          $scope.$on(
            "$destroy",
            function( event ) {
              console.log("Cancelling timer " + $scope.timer);
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

      ansible.getRollbackPoints({project: projects.selectedProject},
        function(response){
          console.log(response.data);
          $scope.rollbackPoints = response.data;
        }, function(response){
          console.error(response.data)
        });

      $scope.getRestoreWorkflowStatus();

      $scope.gettingAnsiblePlaybooks = true;

      $scope.restorePoint = projects.selectedProject.restorePoint;

      ansible.getAnsiblePlaybooksList({project: projects.selectedProject}, function(response){
        $scope.gettingAnsiblePlaybooks = false;
        $scope.ansiblePlaybooks = response.data;

        angular.forEach($scope.ansiblePlaybooks,function(ansibleplaybook) {

          var tempWorkflow = angular.copy(baseTile);
          tempWorkflow.title = ansibleplaybook.split(".")[0].toUpperCase();
          tempWorkflow.objectType = ansibleplaybook.split(".")[0];
          tempWorkflow.state = 'default';
          tempWorkflow.loading = true;

          var workflowFound = false;
          angular.forEach($scope.workflows, workflow => {
            if(workflow.title === tempWorkflow.title){
              $scope.getansibleInfo(workflow);
              workflowFound = true;
            }
          });

          if(!workflowFound){
            $scope.workflows.push(tempWorkflow);
            $scope.getansibleInfo(tempWorkflow);
          }
        });

      }, function(response){
        $scope.gettingAnsiblePlaybooks = false;
        toasts.showError(response.data, 'Error', 'red');
      })
    };


    /**
     * Get Restore Workflow Status
     */
    $scope.restoreWorkflow = angular.copy(baseTile);
    $scope.restoreWorkflow.title = '_rollback-ehc'.toUpperCase();
    $scope.restoreWorkflow.objectType = '_rollback-ehc';
    $scope.restoreWorkflow.state = 'default';
    $scope.restoreWorkflow.loading = true;

    $scope.getRestoreWorkflowStatus = function(){

      ansible.get(projects.selectedProject._id, '_rollback-ehc', function(successResponse) {
          $scope.restoreWorkflow.loading = false;
          if(!successResponse.data || !successResponse.data.length)return;
          $scope.restoreWorkflow.jobObject = successResponse.data[successResponse.data.length - 1];
          $scope.restoreWorkflow.jobObjects = successResponse.data;
          $scope.restoreWorkflow.buttonText = 'Configure';

          var workflowFound = false;
          angular.forEach($scope.workflows, workflow => {
            if(workflow.title === $scope.restoreWorkflow.title){
              $scope.getansibleInfo(workflow);
              workflowFound = true;
            }
          });

          if(!workflowFound){
            $scope.workflows.push($scope.restoreWorkflow);
            $scope.getansibleInfo($scope.restoreWorkflow);
          }

        },
        function(errorResponse){
          $scope.restoreWorkflow.loading = false;
          $scope.restoreWorkflow.buttonText = 'Configure';
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data));
          toasts.showError("errorResponse ="+ JSON.stringify(errorResponse.data));
        });

    };

    /**
     * Show Last Good Configurations
     * @param ev
     */
    $scope.showLastGoodConfigurations  = function(ev){

      $mdDialog.show({
        controller: 'LastGoodConfigurationCtrl',
        //component: 'lastGoodConfigurations',
        templateUrl: '/app/ansible/last_good_configurations/last_good_configurations.html',
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

    projects.refresh();

  }
}

angular.module('ehcOzoneApp')
  .component('ansible', {
    templateUrl: 'app/ansible/ansible.html',
    controller: AnsibleComponent
  });

})();
