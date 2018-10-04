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
  .directive('toggleButton', function () {
    return {
      templateUrl: 'app/directives/toggle_button/toggle_button.html',
      restrict: 'EA',
      scope:{
        btnDisabled:'=',
        showIcon:'=',
        hideIcon:'=',
        showState:'=',
        hideState:'=',
        state:'=',
        action:'&'
      },
      link: function (scope, element, attrs) {

        scope.expandIcon = scope.showIcon;
        scope.rotation = 'clock';

        scope.expandRow = function(){
          scope.expandIcon = scope.expandIcon == scope.showIcon ? scope.hideIcon : scope.showIcon;
          scope.state.value = scope.state.value == scope.showState ? scope.hideState : scope.showState;
          scope.rotation = scope.rotation == 'clock' ? 'counterclock' : 'clock';


        }

      }
    };
  });
