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

class DesignComponent {
  constructor($scope,$state,projects,$rootScope,$mdEditDialog) {

    $scope.editMode = false;
    $scope.showPassword = false;
    $scope.import_data = null;

    var componentKey = 'import_data';

    /**
     * Save Project
     */
    $scope.save = function(){

      projects.selectedProject.components.import_data.vars = categoriesToData();
      $scope.import_data = projects.selectedProject.components.import_data;

      $scope.buttonicon = 'refresh';
      projects.updateAnsibleVariableFiles(projects.selectedProject,
        function(response){
          $scope.submitForm();
        },
        function(errorResponse){
          $scope.buttonicon = 'error';
          $scope.buttontheme = 'red';
          $scope.formStatus = 'Fail';
          $scope.errmsg = errorResponse.data;
          toasts.showError(errorResponse.data,"Error saving data", "red")
        }
      );

    };

    /**
     * Edit Mode
     */
    $scope.customEdit = function(){

      projects.getDecryptedProject(projects.selectedProject._id,
        function(successResponse){
          $scope.editMode = true;
          if(successResponse.data.components && successResponse.data.components.import_data.vars)
            loadDesignData(successResponse.data.components.import_data.vars)
        }, function(errorResponse){
          toasts.showError(errorResponse.data,"Error fetching data", "red")
        });

      $scope.edit();

    };


    $scope.isPassword = function(key){
      return (key.indexOf('password') > -1 || key.indexOf('passphrase') > -1)
    };

    /**
     * Cancel Edit Mode
     */
    $scope.cancel = function(){
      //$scope.editMode = false;
      $scope.showPassword = false;
      $scope.cancelForm();
      loadDesignData()
    };

    /**
     * Edit Value
     * @param event
     * @param categoryData
     * @param key
     */
    $scope.editValue = function (event, categoryData, key) {

      // if auto selection is enabled you will want to stop the event
      // from propagating and selecting the row
      event.stopPropagation();

      var promise = $mdEditDialog.small({
        // messages: {
        //   test: 'I don\'t like tests!'
        // },
        modelValue: JSON.stringify(categoryData[key]),
        placeholder: JSON.stringify(categoryData[key]),
        title: 'Edit value - Hit ENTER to save, or ESC to cancel',
        type: $scope.isPassword(key) && !$scope.showPassword && 'password',
        save: function (input) {
          try{
            categoryData[key] = JSON.parse(input.$modelValue);
          }catch(e){
            categoryData[key] = input.$modelValue;
          }
        },
        targetEvent: event,
      });

      promise.then(function (ctrl) {
        var input = ctrl.getInput();

        input.$viewChangeListeners.push(function () {
          input.$setValidity('test', input.$modelValue !== 'test');
        });
      });
    };


    /**
     * categoriesToData
     * @param designData
     */
    var categoriesToData = function(){
      var result = {};
      angular.forEach($scope.categories,function(category){
        result[category.component] = category.data;
      });

      return result;

    };

    /**
     * Convert Data from JSON format to different array of categories
     * @param designData
     */
    var dataToCategories = function(designData){
      $scope.categories = [];
      $scope.selectedCategory = null;

      angular.forEach(designData,function(value,key){

        var varObject = {
          name: key.replace(/_/g," "),
          component: key,
          data: value
        };

        $scope.categories.push(varObject);

        if(key == 'common'){
          $scope.selectedCategory = varObject;
        }

      });

      if(!$scope.selectedCategory){
        $scope.selectedCategory = $scope.categories[0]
      }
    };


    /**
     * Load Design Data
     */
    var loadDesignData = function(designData){

      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.import_data && projects.selectedProject.components.import_data.vars)
        designData = designData || projects.selectedProject.components.import_data.vars;

      dataToCategories(designData)

    };


    $scope.go = function(route){
      $state.go(route)
    };

    projects.refresh();

    $scope.projectSelected = false;
    $rootScope.$on('notifying-project-change',function(){
      $scope.projectSelected = true;
    });

    projects.initializeFormActions($scope, componentKey);
    projects.subscribe($scope, componentKey, function(){
      loadDesignData();
    });


  }
}

angular.module('ehcOzoneApp')
  .component('design', {
    templateUrl: 'app/design/design.html',
    controller: DesignComponent
  });

})();
