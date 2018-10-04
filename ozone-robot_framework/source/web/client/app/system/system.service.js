'use strict';

angular.module('ehcOzoneApp')
  .service('system', function ($http, $mdDialog, $rootScope) {
    // AngularJS will instantiate a singleton by calling "new" on this function


    const api = '/api/system';
    const servicesApi = '/api/system/services';
    const serviceStartApi = '/api/system/services/start';
    const masterPasswordCheckApi = '/api/system/password/isset';
    const masterPasswordApi = '/api/system/password';
    const agentAPI = '/api/system/agent';
    const queueJobsAPI = '/api/system/queue/jobs';
    const requeueJobsAPI = '/api/system/queue/requeue';
    const cleanupJobsAPI = '/api/system/queue/cleanup';


    /**
     * Get List of services and their status
     * @param successCallback
     * @param errorCallback
     */
    this.getServiceList = function(successCallback, errorCallback){
      $http.get(servicesApi).then(successCallback, errorCallback);
    };

    /**
     * Get Agent Information
     * @param successCallback
     * @param errorCallback
     */
    this.getAgentInfo = function(successCallback, errorCallback){
      $http.get(agentAPI).then(successCallback, errorCallback);
    };

    /**
     * Get Queue Job Stats
     * @param successCallback
     * @param errorCallback
     */
    this.getQueueStats = function(successCallback, errorCallback){
      $http.get(queueJobsAPI).then(successCallback, errorCallback);
    };

    /**
     * Re-queue stuck active jobs
     * @param successCallback
     * @param errorCallback
     */
    this.reQueueJobs = function(successCallback, errorCallback){
      $http.post(requeueJobsAPI).then(successCallback, errorCallback);
    };

    this.cleanupQueue = function(successCallback, errorCallback){
      $http.post(cleanupJobsAPI).then(successCallback, errorCallback);
    };

    /**
     * Start Services
     * @param successCallback
     * @param errorCallback
     */
    this.startServices = function(successCallback, errorCallback){
      $http.post(serviceStartApi).then(successCallback, errorCallback);
    };

    /**
     * Check If Master Password
     * @param successCallback
     * @param errorCallback
     */
    this._checkMasterPassword = function(successCallback, errorCallback){
      $http.get(masterPasswordCheckApi).then(successCallback, errorCallback);
    };

    /**
     * Set Master Password
     * @param successCallback
     * @param errorCallback
     */
    this.setMasterPassword = function(masterPassword, successCallback, errorCallback){
      $http.post(masterPasswordApi, {masterPassword: masterPassword}).then(successCallback, errorCallback);
    };


    /**
     * Check if Master Password is set
     */
    this.checkMasterPassword = function(){
      var THIS = this;
      this._checkMasterPassword (function(response){
          $rootScope.isMasterPasswordSet = true;
      }, function(errorResponse){
        if(errorResponse.data == 'Master Password Not Set'){
          THIS.showSetMasterPasswordDialog();
          $rootScope.isMasterPasswordSet = false;
        }
      })
    };


    var isDlgOpen = false;
    /**
     * Set Master Password
     */
    this.showSetMasterPasswordDialog = function(){

      if (isDlgOpen) return;
      isDlgOpen = true;

      $mdDialog.show({
        template: '<md-dialog aria-label="Dialog" md-theme="red">' +
        '<md-toolbar class="md-primary md-hue-2">' +
        '<div class="md-toolbar-tools">' +
        '  <md-icon ng-md-icon icon="security"></md-icon>     ' +
        '<h2> Master Password </h2>' +
        '<span flex></span>' +
        '<md-button class="md-icon-button" ng-click="closeDialog()">' +
        'x' +
        '</md-button>' +
        '</div>' +
        '</md-toolbar>' +
        '  <md-dialog-content layout-padding style="overflow-wrap: break-word;">' +
        '<form name="passwordForm" ng-hide="passwordReset">' +
        '   <div>' +
        '   <md-input-container>' +
        '     <label>Master Password</label>' +
        '       <input name="masterPassword" ng-model="masterPassword" required minlength="5" type="password" style="width:400px;"/>' +
        '       <div ng-messages="passwordForm.masterPassword.$error" ng-show="passwordForm.masterPassword.$dirty">' +
        '       <div ng-message="required">This is required!</div>' +
        '       <div ng-message="minlength">That is too short!</div>' +
        '   </md-input-container>' +
        '</div>' +
        '   </div>' +
        '   <div>' +
        '   <md-input-container>' +
        '     <label>Confirm Master Password</label>' +
        '       <input ng-model="masterPasswordConfirm" required minlength="5" type="password" style="width:400px;"/>' +
        '   </md-input-container>' +
        '   </div>' +
        '       <div style="width:400px;" class="hint" >This password will be used to secure Redis, Ansible and to encrypt passwords in the database and will also reset current users password. This password will be required to start remote Agent server.</div>' +
        '   <div ng-if="err_msg" layout-margin class="alert alert-danger">' +
        '     {{err_msg}}' +
        '   </div>' +
        '</form>' +
        '<div ng-show="passwordReset">' +
        ' <h4>User password has also been reset. Please use this password going forward to login to this account.</h4>' +
        '</div>' +
        '  </md-dialog-content>' +
        '  <md-dialog-actions style="min-height: 70px;">' +
        '    <md-button ng-hide="passwordReset" ng-disabled="!(masterPassword && masterPassword == masterPasswordConfirm)" ng-click="submitMasterPassword()" class="md-primary">' +
        '      Submit' +
        '    </md-button>' +
        '    <md-button ng-click="closeDialog()" class="md-primary">' +
        '      Close' +
        '    </md-button>' +
        '  </md-dialog-actions>' +
        '</md-dialog>',
        controller: DialogController
      });
      function DialogController($scope, $mdDialog, system, Auth) {
        $scope.masterPassword = '';
        $scope.err_msg = null;
        /**
         * Close Dialogue
         */
        $scope.closeDialog = function () {
          $mdDialog.hide();
          isDlgOpen = false;
        };

        /**
         * Submit Master Password
         */
        $scope.submitMasterPassword = function(){
          system.setMasterPassword($scope.masterPassword, function(){

            // Change user password to match master password
            Auth.changePassword('', $scope.masterPassword)
              .then(() => {
                console.log('User Password successfully changed.');
              })
              .catch(() => {
                console.error("User Resetting User Password.");
              });

            //$scope.closeDialog();
            $scope.passwordReset = true;
            system.checkMasterPassword();
            // Attempt to Start Services
            system.startServices(function(successResponse){

            }, function(errorResponse){
              console.error("Error Starting Services " + errorResponse.data);
            })
          }, function(response){
            $scope.err_msg = response.data;
          });
        }

      }

    }


  });
