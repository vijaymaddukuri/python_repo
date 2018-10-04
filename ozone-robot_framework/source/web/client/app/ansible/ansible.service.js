'use strict';

angular.module('ehcOzoneApp')
  .service('ansible', function ($http, toasts) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    const uri = '/api/ansible';
    const listTasksUri = uri+'/playbook_tasks';
    const listPlaybooksUri = uri+'/playbooks';
    const rollbackPointsUri = uri+'/roll_back_points';
    const ansibleExecutePlaybookUri = uri+'/execute';
    const ansibleExecuteStopUri = uri+'/stop';
    const ansibleExecuteKillUri = uri+'/kill';

    this.create = function(ansibleData,successCallback,errorCallback){
      $http.post(uri,ansibleData).then(successCallback,errorCallback)
    };

    this.get = function(projectid,type,successCallback,errorCallback, limit, skip){
      var params = {projectId: projectid};
      if(type){
        params = {refid:projectid+"_"+type}
      }

      params['limit'] = limit;
      params['skip'] = skip;

      return $http.get(uri,{params:params}).then(successCallback,errorCallback);
    };

    this.getTotalJobs = function(successCallback,errorCallback){
      $http.get(uri + '/total_rows').then(successCallback,errorCallback);
    };

    this.show = function(ansibleId,successCallback,errorCallback){
      $http.get(uri + '/' + ansibleId).then(successCallback,errorCallback);
    };

    this.delete = function(ansibleId,successCallback,errorCallback){
      $http.delete(uri + '/' + ansibleId).then(successCallback,errorCallback);
    };

    this.getLogs = function(ansibleData,successCallback,errorCallback){
      $http.get(uri+'/'+ansibleData._id+'/logs').then(successCallback,errorCallback);
    };

    this.getAnsibleTasksList = function(ansibleData,successCallback,errorCallback){
      $http.post(listTasksUri, ansibleData).then(successCallback,errorCallback);
    };

    this.getAnsiblePlaybooksList = function(ansibleData,successCallback,errorCallback){
      $http.post(listPlaybooksUri, ansibleData).then(successCallback,errorCallback);
    };

    this.getRollbackPoints = function(ansibleData,successCallback,errorCallback){
      $http.post(rollbackPointsUri, ansibleData).then(successCallback,errorCallback);
    };

    this.executeAnsiblePlayBook = function(ansibleData,successCallback,errorCallback){
      $http.post(ansibleExecutePlaybookUri, ansibleData).then(successCallback,errorCallback);
    };

    this.stopAnsiblePlayBookExecution = function(ansibleData,successCallback,errorCallback){
      $http.post(ansibleExecuteStopUri, ansibleData).then(successCallback,errorCallback);
    };

    this.killAnsiblePlayBookExecution = function(ansibleData,successCallback,errorCallback){
      $http.post(ansibleExecuteKillUri, ansibleData).then(successCallback,errorCallback);
    };

    this.showAgentLogsPopup = function(){
      toasts.showLogs('Fetching Logs....', 'Agent Logs', 'blue', 'bottom right');
    }

  });
