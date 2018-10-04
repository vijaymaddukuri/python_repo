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
  .directive('statusLabel', function () {
    return {
      templateUrl: 'app/directives/status_label/status_label.html',
      restrict: 'EA',
      scope:{
        defaultText : '=',
        state: '=',
        completedText : '=?',
        successText : '=?',
        progressText: '=?',
        statusMap: '=?',
        iconSize: '=',
        progress: '=?'
      },
      link: function (scope, element, attrs) {
        //scope.statusTheme = 'default';
        scope.statusTheme = 'default';
        scope.statusText = scope.defaultText;
        scope.successText = scope.successText || scope.completedText;

        var getStatusMap = function(){
          return {
            'LOADING': {icon: 'refresh', theme:'', text: 'Loading'},
            'SUCCESS': {icon: 'done', theme:'green', text: scope.successText || 'SUCCESS'},
            'COMPLETE': {icon: 'done', theme:'green', text: 'SUCCESS'},
            //'COMPLETE': {icon: '', theme:'grey', text: 'COMPLETE'},
            'WARNING': {icon: 'done_all', theme:'orange', text: scope.completedText || 'COMPLETED'},
            'FAIL': {icon: 'error', theme:'red', text: scope.state},
            'FAILED': {icon: 'error', theme:'red', text: scope.state},
            'KILLED': {icon: 'error', theme:'red', text: scope.state},
            'STOPPED': {icon: 'error', theme:'red', text: 'STOPPED'},
            'ERROR': {icon: 'error', theme:'red', text: scope.state},
            'RUNNING': {icon: 'refresh', theme:'default', text: scope.progressText || 'RUNNING'},
            'ACTIVE': {icon: 'refresh', theme:'default', text: scope.progressText || 'RUNNING'},
            'SKIPPED': {icon: 'redo', theme:'grey', text: 'Skipped'},
            'UNREACHABLE': {icon: 'error', theme:'red', text: 'Unreachable'},
            'QUEUED': {icon: 'hourglass_empty', theme:'grey', text: 'Queued'},
            'UNKNOWN': {icon: 'error', theme:'grey', text: 'UNKNOWN'},
            'STOPPING': {icon: 'refresh', theme:'red', text: 'STOPPING'},
            'KILLING': {icon: 'refresh', theme:'red', text: 'KILLING'},
            'NOT RUN': {icon: 'error', theme:'grey', text: 'NOT RUN'}
          }
        };


        var statusMap = scope.statusMap || getStatusMap();

        scope.$watch('state',function(newValue){

          statusMap = scope.statusMap || getStatusMap();

          newValue = newValue && newValue.toUpperCase();

          if(newValue in statusMap){
            scope.statusIcon = statusMap[newValue]['icon'];
            scope.toolTip = scope.toolTipText;
            scope.statusTheme = statusMap[newValue]['theme'] || 'default';
            scope.statusText = statusMap[newValue]['text'] || scope.defaultText || 'UNKNOWN';
          }else{
            scope.toolTip = scope.toolTipText;
            scope.statusTheme = 'default';
            scope.statusText = scope.defaultText || 'UNKNOWN';
          }

        })

      }
    };
  });
