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
  .directive('playButton', function () {
    return {
      templateUrl: 'app/directives/play_button/play_button.html',
      restrict: 'EA',
      scope:{
        action : '&',
        toolTipText : '=',
        state : '=',
        defaultText: '=',
        progressText: '=',
        completedText: '=',
        disabled: '=',
        mdRaised: '=?'
      },
      link: function (scope, element, attrs) {

        scope.mdRaised = angular.isDefined(scope.mdRaised) ? scope.mdRaised : 'md-raised';

        scope.buttontheme = 'default';
        scope.buttonicon = 'play_circle_fill';
        scope.buttonText = scope.defaultText;
        scope.toolTip = scope.toolTipText;

        scope.$watch('state',function(newValue){
          if(newValue === 'SUCCESS'){
            scope.buttonicon = 'done_all';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'green';
            scope.buttonText = scope.completedText;
          }else if(newValue === 'COMPLETE'){
            scope.buttonicon = '';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'grey';
            scope.buttonText = 'COMPLETED';
          }else if(newValue === 'WARNING'){
            scope.buttonicon = 'done_all';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'orange';
            scope.buttonText = scope.completedText;
          }else if(newValue === 'FAIL'){
            scope.buttonicon = 'error';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'red';
            scope.buttonText = 'FAIL';
          }else if(newValue === 'RUNNING'){
            scope.buttonicon = 'refresh';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'blue';
            scope.buttonText = scope.progressText;
          }else if(newValue === 'SKIPPED'){
            scope.buttonicon = 'redo';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'grey';
            scope.buttonText = 'Skipped';
          }else if(newValue === 'UNREACHABLE'){
            scope.buttonicon = 'error';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'red';
            scope.buttonText = 'Unreachable';
          }else if(newValue === 'QUEUED'){
            scope.buttonicon = 'hourglass_empty';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'grey';
            scope.buttonText = 'Queued';
          }else {
            scope.buttonicon = 'play_circle_fill';
            scope.toolTip = scope.toolTipText;
            scope.buttontheme = 'default';
            scope.buttonText = scope.defaultText;
          }

        })

      }
    };
  });
