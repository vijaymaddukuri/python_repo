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
  .controller('ToastsCtrl', function ($scope, $mdToast, $filter, $mdDialog, isDlgOpen, errMsg, title, theme, log, system) {

    /**
     * Close Toast
     */
    $scope.closeToast = function() {
      if (isDlgOpen) return;
      $mdToast
        .hide()
        .then(function() {
          isDlgOpen = false;
        });
    };

    /**
     * Open More Info
     */
    $scope.openMoreInfo = function(){
      log.openMoreInfo(isDlgOpen, errMsg, title, theme);
    };

    if (errMsg && errMsg.indexOf('agentError: ERR invalid password') > -1){
      system.showSetMasterPasswordDialog();
    }


  });

