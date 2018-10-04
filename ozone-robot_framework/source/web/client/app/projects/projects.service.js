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
  .service('projects', function ($http,$rootScope,general,ngProgressFactory,popup,toasts,$location) {
    // AngularJS will instantiate a singleton by calling 'new' on this function

    this.progressbar = ngProgressFactory.createInstance();
    this.progressbar.setHeight('2px');

    var uri = '/api/projects';

    this.selectedProject = null;
    this.defaultConfigData = null;


    /**
     * Create project - Send a Post Request
     * @param project
     * @param successCallback
     * @param errorCallback
     */
    this.createProject = function(project,successCallback,errorCallback){
      $http.post(uri,project).then(successCallback,errorCallback);
    };

    /**
     * Get Projects
     * @param successCallback
     * @param errorCallback
     */
    this.getProjects = function(successCallback,errorCallback){
      var THIS = this;
      this.progressbar.start();
      $http.get(uri).then(function(response){
        THIS.progressbar.complete();
        successCallback(response)
      },function(response){
        THIS.progressbar.complete();
        errorCallback(response)
      })
    };

    /**
     * Show Project
     * @param projectID
     * @param successCallback
     * @param errorCallback
     */
    this.getProject = function(projectID,successCallback,errorCallback){
      //this.progressbar.start();
      $http.get(uri+"/"+projectID).then(successCallback,errorCallback);
    };

    /**
     * Get Project details with decrypted passwords
     * @param projectID
     * @param successCallback
     * @param errorCallback
     */
    this.getDecryptedProject = function(projectID,successCallback,errorCallback){
      //this.progressbar.start();
      $http.get(uri+"/decrypted_data/"+projectID).then(successCallback,errorCallback);
    };

    /**
     * Update Project
     * @param project
     * @param successCallback
     * @param errorCallback
     */
    this.update = function(project,successCallback,errorCallback){
      $http.put(uri+"/"+project._id,project).then(successCallback,errorCallback);
    };

    /**
     * Update Ansible Variables
     * @param project
     * @param successCallback
     * @param errorCallback
     */
    this.updateAnsibleVariableFiles = function(project,successCallback,errorCallback){
      $http.post(uri+"/update_ansible_variable_files",project).then(successCallback,errorCallback);
    };

    /**
     * Update/ Refresh Ansible playbook files from template directory - excluding all group variable
     * @param project
     * @param successCallback
     * @param errorCallback
     */
    this.updateAnsiblePlaybookFiles = function(project,successCallback,errorCallback){
      $http.post(uri+"/update_ansible_playbook_files",project).then(successCallback,errorCallback);
    };

    /**
     * Delete a Project
     * @param selectedProject
     * @param successCallback
     * @param errorCallback
     * @returns {Promise.<TResult>}
     */
    this.deleteProject = function(selectedProject,successCallback,errorCallback){
      return $http.delete(uri+"/"+selectedProject._id).then(successCallback,errorCallback)
    };

    /**
     * Subscribe to project selection changes
     * When a user selects a project this sends out a notification and reloads data
     * @param scope
     * @param componentKey
     * @param callback
     */
    this.subscribe = function(scope, componentKey, callback) {
      var THIS = this;
      var handler = $rootScope.$on('notifying-project-change', function(){
        THIS.setComponentData(scope,componentKey,callback)
      });

      this.setComponentData(scope,componentKey,callback);
      scope.$on('$destroy', handler);
      if(this.selectedProject == null){

        $rootScope.$emit('notify-refresh-projects');
        this.selectedProject = this.projects
      }
    };

    /**
     * A custom subscribe call with a callback.
     * When a user selects a project the callback is called unlike the previous function
     * @param scope
     * @param callback
     */
    this.subscribeCustom = function(scope,callback){
      var THIS = this;
      var handler = $rootScope.$on('notifying-project-change', function(){
        callback()
      });
      scope.$on('$destroy', handler);
      if(this.selectedProject == null){

        $rootScope.$emit('notify-refresh-projects');
        this.selectedProject = this.projects
      }
    };

    /**
     * Set Data in current view
     * @param scope
     * @param componentKey
     * @param callback
     */
    this.setComponentData = function(scope,componentKey,callback){
      if(this.selectedProject && this.selectedProject.components && this.selectedProject.components[componentKey]){
        scope[componentKey] = this.selectedProject.components[componentKey]
      }else{
        if(this.defaultConfigData && componentKey in this.defaultConfigData){
          scope[componentKey] = angular.copy(this.defaultConfigData[componentKey]);
          if(this.selectedProject.type){
            scope[componentKey] = angular.copy(this.defaultConfigData[this.selectedProject.type][componentKey]);
          }else{

          }
        }else{
          scope[componentKey] = angular.copy(scope.default_data);
        }
      }

      if(callback)callback()
    };

    /**
     * Notify When project selection is changed
     */
    this.notify =function() {
      $rootScope.$emit('notifying-project-change');
    };



    this.refresh = function(){
      $rootScope.$emit('notify-refresh-projects');
    };

    this.getDefaultConfigData = function(successCallback,errorCallback){
      $http.get(uri + '/get_default_config_data').then(successCallback,errorCallback)
    };

    var ProjectService = this;
    this.refreshDefaultConfigData = function(){
      this.getDefaultConfigData(function(successResponse){
        ProjectService.defaultConfigData = successResponse.data;
      },function(errorResponse){
        console.error(errorResponse);
      });
    };

    this.refreshDefaultConfigData();

    this.initializeFormActions = function(scope, componentKey){
      var THIS = this;
      scope.editMode = false;

      /**
       * Edit Form
       */
      scope.edit  = function(){
        scope[componentKey] = angular.copy(scope[componentKey]);
        scope.buttonicon = '';
        scope.buttontheme = 'default';
        scope.buttontext = 'Save';
        scope.resetbuttonicon = '';
        scope.editMode = true;
        scope.formStatus = 'edit';
      };

      /**
       * Cancel Form - Reset data
       */
      scope.cancelForm = function(){
        if(scope.editMode) {

          if (THIS.selectedProject.components[componentKey]) {
            scope[componentKey] = THIS.selectedProject.components[componentKey];
          }
          scope.buttonicon = '';
          scope.buttontheme = 'default';
          scope.buttontext = 'Save';
          scope.resetbuttonicon = '';
          scope.editMode = false;
        }
      };

      /**
       * Reset Form
       * @param ev
       */
      scope.resetForm = function(ev){
        if(!THIS.selectedProject.type){
          return popup.showAlert(ev,"Project Type","Project Type not set. Please set a project type in the Projects section")
        }
        if(THIS.defaultConfigData && THIS.defaultConfigData[THIS.selectedProject.type] && componentKey in THIS.defaultConfigData[THIS.selectedProject.type]){

          scope[componentKey] = angular.copy(THIS.defaultConfigData[THIS.selectedProject.type][componentKey]);
        }else{
          scope[componentKey] = angular.copy(scope.default_data);
        }
        scope.resetbuttonicon = 'check';
      };

      /**
       * Submit Form Action
       */
      scope.submitForm = function(){
        scope.buttonicon = 'refresh';
        if(!THIS.selectedProject){
          scope.buttonicon = 'error';
          scope.buttontext = 'Fail';
          scope.errmsg = 'Please select a project';
          toasts.showError("Please select a project","Please select a project", "red");
          return
        }

        if(!THIS.selectedProject.components){
          THIS.selectedProject.components = {};
        }

        THIS.selectedProject.components[componentKey] =scope[componentKey];

        THIS.update(THIS.selectedProject,scope.successCallback,scope.errorCallback);
      };

      /**
       * Submit Form Success Callback
       * @param successResponse
       */
      scope.successCallback = function(successResponse){
        scope.buttonicon = 'check';
        scope.buttontheme = 'green';
        scope.formStatus = 'success';
        scope.inputData = '';
        setTimeout(function () {
          scope.editMode = false;
          $rootScope.getProjects();
          $location.path('/design');
          scope.$apply();
        }, 1000);

      };

      /**
       * Submit Form Error Callback
       * @param errorResponse
       */
      scope.errorCallback = function(errorResponse){
        console.error("Error Response" + errorResponse);
        scope.buttonicon = 'error';
        scope.buttontheme = 'red';
        scope.formStatus = 'Fail';
        scope.errmsg = errorResponse.data;
        toasts.showError(errorResponse.data,"Error saving data", "red")
      }

    }

  });
