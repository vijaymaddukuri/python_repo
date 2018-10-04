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
  .directive('ansibleRunner', function ($mdDialog) {
    return {
      templateUrl: 'app/directives/ansible_runner/ansible_runner.html',
      restrict: 'EA',
      scope:{
        component: '=',
        configureObject: '&'
      },
      link: function (scope, element, attrs) {

          scope.showExecutionModal = function(ev) {

            $mdDialog.show({
              controller: 'AnsibleExecutorCtrl',
              templateUrl: '/app/directives/ansible_runner/execute_ansible.html',
              parent: angular.element(document.body),
              targetEvent: ev,
              clickOutsideToClose: false,
              locals: {
                component: scope.component,
                configureObject: scope.configureObject
              },
            });
          };

      }
    };
  });
