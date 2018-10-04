'use strict';
(function(){

class AllRunsComponent {
  constructor($scope, ansible, toasts, projects, time, $timeout, $mdDialog) {

    $scope.selectedJobs = [];
    $scope.allAnsibleJobs = [];

    $scope.query = {
      order: '-jobId',
      limit: 10,
      page: 1
    };

    /**
     * Get Ansible Jobs Information
     * @returns {null}
     */
    $scope.getansibleInfo = function(){
      $scope.dataLoaded = true;

      if(!projects.selectedProject)return null;
      $scope.gettingAnsibleJobs = true;
      $scope.promise = ansible.get(projects.selectedProject._id, null , function(successResponse) {
          $scope.gettingAnsibleJobs = false;

          $scope.allAnsibleJobs = successResponse.data;
          $scope.allAnsibleJobs && $scope.allAnsibleJobs.map(ansibleJob => {
            ansibleJob.timeDifference = $scope.getTimeDifference(_getTimeDifference(ansibleJob));
          });

          $scope.allAnsibleJobs = $scope.allAnsibleJobs && $scope.allAnsibleJobs.reverse();

          $scope.getPageData();
          //$scope.ansibleJobs = $scope.allAnsibleJobs

          //refreshJobs();

        },
        function(errorResponse){
          $scope.gettingAnsibleJobs = false;
          toasts.showError(errorResponse.data, 'Error', 'red');
          console.error("errorResponse ="+ JSON.stringify(errorResponse.data));
          refreshJobs();
        });
    };

    /**
     * Get Page Data
     */
    $scope.getPageData = function(){
      $scope.ansibleJobs = $scope.allAnsibleJobs && $scope.allAnsibleJobs.slice($scope.query.limit * ($scope.query.page-1), $scope.query.limit * ($scope.query.page));
    }

    /**
     * Get Time Difference
     * If duration exists in job, meaning the job has finished , then use duration to display time
     * Else if job is running calculate difference from job start time
     */
    var _getTimeDifference = function (ansibleJob) {

      if (ansibleJob.duration) return ansibleJob.duration;
      else return (new Date() - new Date(ansibleJob.date));

    };

    /**
     * Refresh Jobs
     */
    var refreshJobs = function(){

      $scope.refreshTimer = $timeout(function () {
        $scope.getansibleInfo();
      }, 30000);

      // On scope destroy cancel timeout
      $scope.$on('$destroy', function () {
        // Make sure that the timer is destroyed
        $timeout.cancel( $scope.refreshTimer );
      });

    };

    /**
     * Get Time Difference
     * @param difference
     */
    $scope.getTimeDifference = function(difference){
      return difference && time.getTimeDifference(difference)
    };

    /**
     * Stop Job
     * @param ansibleJob
     */
    $scope.stopJob = function(ansibleJob){
      ansible.stopAnsiblePlayBookExecution(ansibleJob,
        function(response){
          $scope.getansibleInfo();
      }, function(responseerrorResponse){
          toasts.showError(responseerrorResponse.data, 'Error', 'red');
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
      })
    };


    /**
     * Show stop workflow dialogue
     * @param ev
     * @param ansibleJob
     */
    $scope.showStopJobDialog = function(ev, ansibleJob){

      var confirm = $mdDialog.confirm()
        .title('Confirm')
        .textContent('Are you sure you want to stop the workflow execution? The job will finish after the current task is complete')
        .ariaLabel('Stop')
        .targetEvent(ev)
        .ok('Yes')
        .cancel('No');
      $mdDialog.show(confirm).then(function () {
        $scope.stopJob(ansibleJob)
      }, function () {
        // Dialogue Cancel Action
      });
    };

    /**
     * Show Kill Job Dialogue
     * @param ev
     * @param ansibleJob
     */
    $scope.showKillJobDialog = function(ev, ansibleJob){

      var confirm = $mdDialog.confirm()
        .title('Confirm')
        .textContent('Are you sure you want to kill the workflow execution? This process will be terminated but any remote processes initiated by this process may still be running.')
        .ariaLabel('Kill')
        .targetEvent(ev)
        .ok('Yes')
        .cancel('No');
      $mdDialog.show(confirm).then(function () {
        $scope.killJob(ansibleJob)
      }, function () {
        // Dialogue Cancel Action
      });
    };

    /**
     * Show Delete Job Dialogue
     * @param ev
     * @param ansibleJob
     */
    $scope.showDeleteJobDialog = function(ev){

      var confirm = $mdDialog.confirm()
        .title('Confirm')
        .textContent('Are you sure you want to delete the selected jobs?')
        .ariaLabel('Delete')
        .targetEvent(ev)
        .ok('Yes')
        .cancel('No');
      $mdDialog.show(confirm).then(function () {
        $scope.deleteSelectedJobs()
      }, function () {
        // Dialogue Cancel Action
      });
    };

    /**
     * Delete Job
     * @param ansibleJob
     */
    $scope.deleteJob = function(ansibleJob, index){
        ansible.delete(ansibleJob._id, function(){
          // $scope.ansibleJobs.splice(index, 1);
          //$scope.getansibleInfo()
        }, function(errorResponse){
          toasts.showError(errorResponse.data, 'Error', 'red');
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
        })
    }

    /**
     * Delete Selected Jobs
     */
    $scope.deleteSelectedJobs = function(){
      $scope.selectedJobs.map((selectedJob) => {
        $scope.deleteJob(selectedJob);
      })
      $scope.getansibleInfo();
    }

    /**
     * Kill Job
     * @param ansibleJob
     */
    $scope.killJob = function(ansibleJob){
      ansible.killAnsiblePlayBookExecution(ansibleJob,
        function(response){
          $scope.getansibleInfo();
        }, function(errorResponse){
          toasts.showError(errorResponse.data, 'Error', 'red');
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
        })
    };



    /**
     * Subscribe to project change
     */
    projects.subscribeCustom($scope,$scope.getansibleInfo);

    if(!$scope.dataLoaded){
      $scope.getansibleInfo()
    }

  }
}

angular.module('ehcOzoneApp')
  .component('allRuns', {
    templateUrl: 'app/ansible/all_runs/all_runs.html',
    controller: AllRunsComponent
  });

})();
