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
  .directive('customDataTable', function (projects, $mdEditDialog) {
    return {
      templateUrl: 'app/directives/custom_data_table/custom_data_table.html',
      restrict: 'EA',
      scope:{
        componentKey: '=',
        customData: '='
      },
      link: function (scope, element, attrs) {

        //scope.vars = scope.dataObjectVariable;
        scope.vars = scope.customData;

        projects.initializeFormActions(scope, scope.componentKey);
        projects.subscribe(scope, scope.componentKey);

        scope.editValue = function (event, vars, key) {

          event.stopPropagation();

          var promise = $mdEditDialog.large({
            modelValue: vars[key],
            placeholder: '',
            title: 'Edit Value',
            save: function (input) {
              vars[key] = input.$modelValue;
            },
            targetEvent: event,
            validators: {
              'md-maxlength': 30
            }
          });

          promise.then(function (ctrl) {
            var input = ctrl.getInput();

            input.$viewChangeListeners.push(function () {
              input.$setValidity('test', input.$modelValue !== 'test');
            });
          });
        };

      }
    };
  });
