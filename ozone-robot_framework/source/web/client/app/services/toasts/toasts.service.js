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
  .service('toasts', function ($mdToast) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    this.showError = function(errMsg, title, theme, position){

      if(!errMsg){
        console.error("Error Message is blank. So not showing error toast");
        return
      }

      position = position || 'top right';

      $mdToast.show({
        hideDelay   : 0,
        position    : position,
        controller  : 'ToastsCtrl',
        locals : {
          isDlgOpen: false,
          errMsg : errMsg,
          title: title,
          theme: theme
        },
        template : '<md-toast>' +
                      '<span class="md-toast-text" flex>' + title + '</span>' +
                        '<md-button class="md-highlight" ng-click="openMoreInfo($event)">' +
                          'More info' +
                        '</md-button>' +
                        '<md-button ng-click="closeToast()">' +
                          'Close' +
                          '</md-button>' +
                    '</md-toast>'
      });
    };

    this.showLogs = this.showError;

  });
