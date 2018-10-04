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
(function () {

  class ImportComponent {
    constructor($scope, projects, toasts) {

      $scope.searchText = "";
      $scope.showCurrentData = {value: false};

      $scope.selectedProject = JSON.stringify(projects.selectedProject, null, '\t');
      $scope.import = {
        buttonicon: 'file_download'
      };

      $scope.default_data = {};
      var componentKey = 'import_data';
      $scope.import_data = "Loading...";

      /**
       * Get Decrypt Data from server
       */
      $scope.getDesignData = function () {

        $scope.selectedProject = JSON.stringify(projects.selectedProject, null, '\t');

        if (!(projects.selectedProject && projects.selectedProject._id)) {
          $scope.import_data = $scope.default_data;
          return null;
        }
      };

      //$scope.edit();

      /**
       * Convert Input String to JSON Object
       * @param inputString - String in format - host.automation_pod_sso.hostname=host.ehcdomain2.local
       * @returns {Object|null} {host:{automation_pod_sso: {hostname: 'host.ehcdomain2.local'}}}
       */
      var getJsonObjectFromDottedString = function (tempObject, inputString) {

        if (inputString.indexOf('=') < 0) {
          return;
        }

        var keyPart = inputString.split('=')[0];

        if (keyPart.indexOf('.') > -1) {

          var firstKeyPart = keyPart.split('.')[0];
          if(keyPart.split('.').length > 1){
            var secondKeyPart = keyPart.split('.')[1];
          }

          if (tempObject[firstKeyPart] == null) {
            if(secondKeyPart && !isNaN(secondKeyPart)){
              tempObject[firstKeyPart] = [];
              tempObject[firstKeyPart][secondKeyPart] = {};
              getJsonObjectFromDottedString(tempObject[firstKeyPart][secondKeyPart], inputString.split(/\.(.+)?/)[1].split(/\.(.+)?/)[1])
            }else{
              tempObject[firstKeyPart] = {};
              getJsonObjectFromDottedString(tempObject[firstKeyPart], inputString.split(/\.(.+)?/)[1])
            }
          }else{
            getJsonObjectFromDottedString(tempObject[firstKeyPart], inputString.split(/\.(.+)?/)[1])
          }

        } else {
          // Check if key is a number to see if its an array
          if (!isNaN(keyPart)) {

            // If array is not initialized
            if (!Array.isArray(tempObject)) {
              tempObject = [];
              tempObject[parseInt(keyPart)] = inputString.split(/=(.+)?/)[1] || ""
            }

          } else {
            tempObject[keyPart] = inputString.split(/=(.+)?/)[1] || ""
          }
        }
        return tempObject;
      };

      /**
       * Process Data
       * Convert Input data to JSON Data
       */
      $scope.processData = function () {

        $scope.import_data = {
          hosts: [{"name": "localhost"}],
          groups: [],
          vars: {}
        };

        var inputDataLines = $scope.inputData.split("\n");
        for (var index = 0; index < inputDataLines.length; index++) {
          var item = inputDataLines[index];

          // Replace new line characters
          item = item.replace(String.fromCharCode(13), "");

          try {

            if (item && item.indexOf(".") > -1 && item.indexOf("=") > -1) {
              var category = item.split(/\.(.+)?/)[0];

              if (!$scope.import_data.vars[category]) {
                $scope.import_data.vars[category] = {}
              }

              getJsonObjectFromDottedString($scope.import_data.vars[category], item.split(/\.(.+)?/)[1]);

            } else {

              if (item && item != "" && item.indexOf("#") == -1) {
                throw ("Incorrect Format on line " + (index + 1))
              }
            }
          } catch (e) {
            console.log("Input parsing error" + e);
            toasts.showError(e.message, "Input parsing error", "red");
            return
          }
        }


        $scope.outData = "";

        if (!projects.selectedProject.components)
          projects.selectedProject.components = {};

        projects.selectedProject.components.import_data = $scope.import_data;

        $scope.buttonicon = 'refresh';
        projects.updateAnsibleVariableFiles(projects.selectedProject,
          function (response) {
            $scope.submitForm();
          },
          function (errorResponse) {
            $scope.buttonicon = 'error';
            $scope.buttontheme = 'red';
            $scope.formStatus = 'Fail';
            $scope.errmsg = errorResponse.data;
            toasts.showError(errorResponse.data, "Error saving data", "red")
          }
        );
      };

      /**
       * Convert JSON to Input Data
       * Used when data is retreived from server for edit/update purpose
       * @param data
       */
      $scope.jsonToInputData = function (import_data) {

        var vars = import_data.vars;
        var hosts = import_data.hosts;
        var groups = import_data.groups;

        var results = "";

        angular.forEach(vars, function (groupValue, groupName) {

          results += "\n# " + groupName + " variables\n";

          angular.forEach(groupValue, function (value, key) {

            results += (groupName + "." + key + "=" + value + "\n");

          })

        });

        results += "\n# Host Information\n";
        angular.forEach(hosts, function (host) {
          var ip = host.ip || "";
          results += ("host." + host.name + "=" + ip + "\n");
        });

        results += "\n# Group Information\n";
        angular.forEach(groups, function (group) {
          results += ("group." + group.name + "=" + group.members + "\n");
        });

        // $scope.inputData = results;

      };

      $scope.errorReadingExcelFile = function(error){
        $scope.errmsg = 'Error reading Excel file - ' + error;
        toasts.showError($scope.errmsg, 'Error reading Excel file - ' + error, "red");
      };


      /**
       * Get Column Name by Header
       * @param Worksheet
       * @param header
       */
      var getColumnByHeader = function(Worksheet, header){

        for(var i=65;i <= 90; i++ ){
          var column = String.fromCharCode(i);
          var cell = column + "1";
          var value = Worksheet[cell] && Worksheet[cell].v;
          if ( value == header ){
            return column
          }
        }

        // Raise error if column is not found
        throw ('Cannot find column with header - "' + header + '"')

      };

      /**
       * Read Excel File
       * Looks for Sheet name = EHC_VxRail_Input
       * Gets key from
       * Note: Reading formula and values directly from Excel can cause issue. Sometimes characters are replaced. Especially those after _x. eg _x64 gets replaced with d
       */
      $scope.readExcelFile = function(workbook){

        // var sheets = ['EHC_VxRail_Input', 'ESXi_details'];
        var sheets = workbook.SheetNames;

        // Clear existing data
        $scope.inputData = "";

        $scope.warnings = [];
        $scope.errmsgs = [];

        $scope.excel_cell_values = [""];

        for(var i=0; i<sheets.length; i++){
          var sheet_name = sheets[i];

          // Check if workbook has the sheet
          if(!(sheet_name in workbook.Sheets) || !workbook.Sheets[sheet_name]){
            $scope.errmsgs.push('Workbook does not have sheet "' + sheet_name + '"');
            toasts.showError($scope.errmsg, "Error reading data", "red");
            $scope.cancelForm();
            return
          }

          if(sheet_name.indexOf('EHC_') == -1){
            $scope.warnings.push('Skipping sheet "' + sheet_name + '" as name does not contain "EHC_" in it');
            continue
          }

          var Worksheet = workbook.Sheets[sheet_name];
          // TODO: Add some more checks here

          parseExcelSheet(Worksheet, sheet_name)
        }

        $scope.inputData = $scope.excel_cell_values.join("\n");
        $scope.edit();
        $scope.$apply()

      };

      /**
       * Parse Excel Sheet
       * @param Worksheet
       * @param sheet_name
       */
      var parseExcelSheet = function(Worksheet, sheet_name){

        var column_labels = {
          description: "Description",
          supplied_value: "Supplied_Value",
          default_value: "Default_Value",
          group: "Group",
          parameter: "Parameter",
          nested_parameter: "Nested_Parameter"
        };

        try{

          var supplied_value_column = getColumnByHeader(Worksheet, column_labels.supplied_value);
          var default_value_column = getColumnByHeader(Worksheet, column_labels.default_value);
          var group_column = getColumnByHeader(Worksheet, column_labels.group);
          var parameter_column = getColumnByHeader(Worksheet, column_labels.parameter);
          var nested_parameter_column = getColumnByHeader(Worksheet, column_labels.nested_parameter);

        }catch(e){
          $scope.errmsgs.push(e);
          toasts.showError($scope.errmsg, "Error reading data", "red");
          $scope.cancelForm();
          return
        }

        // Identify total number of lines
        var total_lines = Worksheet["!ref"].replace(/.*:.*?(\d+)/,'$1');

        // Start from 2nd Row to the end
        for(var i=2;i<=total_lines; i++){

          // Extract values from raw field as in some cases the values in other fields may be different from what user typed. eg. a value with _x64_ gets replaced by nothing.
          var supplied_value =  Worksheet[supplied_value_column + i] && Worksheet[supplied_value_column + i].r && Worksheet[supplied_value_column + i].r.replace(/<t(.*)>(.*)<\/t>/, "$2") || (Worksheet[supplied_value_column + i] && Worksheet[supplied_value_column + i].v);
          var default_value = Worksheet[default_value_column + i] && Worksheet[default_value_column + i].r && Worksheet[default_value_column + i].r.replace(/<t(.*)>(.*)<\/t>/, "$2") || (Worksheet[default_value_column + i] && Worksheet[default_value_column + i].v);
          var group_value = Worksheet[group_column + i] && Worksheet[group_column + i].v;
          var parameter_value = Worksheet[parameter_column + i] && Worksheet[parameter_column + i].v;
          var nested_parameter_value = Worksheet[nested_parameter_column + i] && Worksheet[nested_parameter_column + i].v;

          if(!group_value || !parameter_value)continue;

          if(group_value == 'Sizing'){
            console.log("sizing")
          }

          var key = group_value + '.' + parameter_value;
          key = key.toLowerCase().replace(/ /g,"_");

          // Nested Parameters are case sensitive. Do not change case
          if(nested_parameter_value) key += '.' + nested_parameter_value;

          var actual_value = supplied_value;

          if(supplied_value == null){
            actual_value = default_value;
          }

          if(actual_value == null){
            $scope.warnings.push('No value in sheet "' + sheet_name + '" row  ' + i);
            actual_value = '';
          }

          try{
            if(actual_value !== ''){
              $scope.excel_cell_values.push(key + "=" + actual_value)
            }
          }
          catch(e){
            $scope.warnings.push('Error parsing sheet "' + sheet_name + '" row  ' + i + ' - ' + e);
          }

        }

      };

      // Initialize actions for Submit button
      projects.initializeFormActions($scope, componentKey);

      // Subscribe to project changes.
      // Whenever user selects a new project refresh design data
      projects.subscribe($scope, componentKey, function () {
        $scope.getDesignData()
      });

    }
  }

  angular.module('ehcOzoneApp')
    .component('import', {
      templateUrl: 'app/design/import/import.html',
      controller: ImportComponent
    });

})();
