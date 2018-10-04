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
  .directive('dataTable', function (projects, $mdEditDialog) {
    return {
      templateUrl: 'app/directives/data_table/data_table.html',
      restrict: 'EA',
      link: function (scope, element, attrs) {

        var componentKey = attrs.componentKey;
        scope.vars = attrs.dataObject;

        projects.initializeFormActions(scope, componentKey);
        projects.subscribe(scope, componentKey);

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
