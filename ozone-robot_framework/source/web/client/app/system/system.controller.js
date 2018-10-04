'use strict';
(function(){

class SystemComponent {
  constructor($scope, system, toasts, log, appConfig) {
    var redisFilterKeys = ['redis_version', 'os', 'process_id', 'tcp_port', 'uptime_in_seconds', 'config_file', 'connected_clients', 'blocked_clients', 'used_memory_human', 'used_memory_peak_human', 'total_system_memory_human', 'rdb_bgsave_in_progress', 'used_cpu_sys'];

    $scope.timespanConfig = {
      lessThanFirst: 'now',   // What to display if the diff is less than the first available unit
      millisecond: false,      // ------------------------------------
      second: false,            //
      minute: 'm',            //
      hour: 'h',              // Labels for each unit, use them for
      day: 'd',               // shorthand units, localization...
      week: 'w',              // Set any to `false` to disable it
      month: 'mo',            //
      year: 'y',              // ------------------------------------
      space: false,           // Whether to add a space between the number and the label
      pluralize: false         // Whether to add an 's' to the label if the diff > 1
    };

    $scope.appConfig = appConfig;
    $scope.requeueJobsIcon = 'repeat';
    $scope.refreshOzoneHealthIcon = '';
    $scope.cleanupJobsIcon = 'delete';

    $scope.services = [];

    /**
     * Get Logs
     * @param type
     */
    $scope.fetchLogs = function (type) {
      log.openMoreInfo(false, 'Fetching', type, 'blue');
    };

    /**
     * Get Queue Statistics
     */
    $scope.getQueueStats = function(){
      $scope.queueErrorMessage = '';
      $scope.queueJobsIcon = 'refresh';
      system.getQueueStats(
        function (response) {
          $scope.queueJobsIcon = 'done';
          $scope.queueStats = response.data;

        }, function (errResponse) {
          $scope.queueJobsIcon = 'error';
          $scope.queueErrorMessage = errResponse.data;
          toasts.showError(errResponse.data, 'Error', 'red');
        });
    };

    /**
     * Re-queue stuck jobs
     * NOTE: ONLY REQUEUE STATUSUPDATE JOBS. REQUEUING EXEC JOBS WILL RESULT IN RE-EXECUTING ANSIBLE JOBS
     * EXEC JOBS STUCK IN ACTIVE STATE MUST BE KILLED AFTER ENSURING THEY ARE STUCK
     */
    $scope.requeueJobs = function(){
      $scope.requeueSuccessMessage = "";
      $scope.requeueErrorMessage = "";
      $scope.requeueJobsIcon = 'refresh';
      system.reQueueJobs(
        function(response){
          $scope.requeueJobsIcon = 'done';
          $scope.requeueSuccessMessage = response.data;
          $scope.getQueueStats();
        },function(response){
          $scope.requeueJobsIcon = 'error';
          $scope.requeueErrorMessage = response.data;
        })
    };

    /**
     * Cleanup Queue
     */
    $scope.cleanupQueue = function(){

      system.cleanupQueue(
        function(response){
          $scope.cleanupJobsIcon = 'done';
          $scope.cleanupSuccessMessage = response.data;
          $scope.getHealthStatus();
        },function(response){
          $scope.cleanupJobsIcon = 'error';
          $scope.cleanupErrorMessage = response.data;
        });

    };

    /**
     * Get Health Status
     */
    $scope.getHealthStatus = function () {
      $scope.refreshOzoneHealthIcon = 'refresh';
      $scope.requeueJobsIcon = 'repeat';
      $scope.refreshOzoneHealthIcon = '';
      $scope.cleanupJobsIcon = 'delete';
      // Running = Getting information
      $scope.redis = {
        state: 'Running'
      };

      // Running = Getting information
      $scope.agentInfo = {
        state: 'Running'
      };

      angular.forEach($scope.services, service => {
        service.status = 'Running'
      });

      /**
       * Get Services list
       */
      system.getServiceList(function (response) {

        $scope.services = response.data.forever.data.map(item => {
          return {
            name: item.id || item.file,
            status: item.running && 'SUCCESS' || 'FAIL',
            type: 'service',
            data: item,
            uptime: (new Date().getTime() - item.ctime),
            logsType: item.id
          }
        });


        $scope.redis = response.data.redis;
        $scope.redis.state = $scope.redis.state && 'SUCCESS' || 'FAIL';
        $scope.redis.logsType = 'redis';


        $scope.redisDataArray = [];

        if ($scope.redis.state) {
          $scope.redisDataArray = angular.forEach($scope.redis.data, (key, value) => {
            $scope.redisDataArray.push({'key': key, 'value': value});
          });

          $scope.redisFilteredDataArray = redisFilterKeys.map(function (key) {
            return {'key': key, 'value': $scope.redis.data[key]}
          });
        }


      }, function (errorResponse) {
        toasts.showError(errorResponse.data, 'Error', 'red');
      });

      /**
       * Get Agent Info
       */
      system.getAgentInfo(
        function (response) {
          $scope.refreshOzoneHealthIcon = '';
          $scope.agentInfo = response.data;
          $scope.agentInfo.state = 'SUCCESS'

        }, function (errorResponse) {
          $scope.refreshOzoneHealthIcon = '';
          $scope.agentInfo.state = 'FAIL';
          $scope.agentInfo.errData = errorResponse.data;
          toasts.showError(errorResponse.data, 'Error', 'red');
        });

      /**
       * Get Queueu Stats
       */
      $scope.getQueueStats();

    };


    $scope.getHealthStatus();

    system.checkMasterPassword();

    $scope.startServicesJobsIcon = 'replay';
    $scope.startServicesError = '';
    $scope.startServices = function(){
      $scope.startServicesError = '';
      $scope.startServicesJobsIcon = 'refresh';
      // Attempt to Start Services
      system.startServices(function(successResponse){
        $scope.startServicesJobsIcon = 'done';
      }, function(errorResponse){
        $scope.startServicesJobsIcon = 'error';
        $scope.startServicesError = errorResponse.data;
        console.error("Error Starting Services " + errorResponse.data);
      })
    }

  }
}

angular.module('ehcOzoneApp')
  .component('system', {
    templateUrl: 'app/system/system.html',
    controller: SystemComponent
  });

})();
