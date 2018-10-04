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

class UpgradeComponent {
  constructor($scope, upgrade, $sce, ansi2html, $mdDialog, $timeout) {

    $scope.showConfirm = function(ev) {
      // Appending dialog to document.body to cover sidenav in docs app
      var confirm = $mdDialog.confirm()
        .title('Upgrade')
        .textContent('Are you sure you want to upgrade? Services will be restarted and any ongoing jobs will be halted.')
        .ariaLabel('Upgrade')
        .targetEvent(ev)
        .ok('Yes')
        .cancel('No');
      $mdDialog.show(confirm).then(function() {
        $scope.upgradeApplication(ev);
      }, function() {

      });
    };


    $scope.getUpgradeInfo = function(){

      upgrade.get(function(successResponse) {

          $scope.upgradeObject = successResponse.data[successResponse.data.length - 1];

          if($scope.upgradeObject && $scope.upgradeObject.logfile){
            var matches = $scope.upgradeObject.logfile.match(/.*_(.*).log/);
            if(matches.length > 1)$scope.logtime = matches[1];
          }

          if($scope.upgradeObject){
            $scope.refreshLogs();
          }
        },
        function(errorResponse){
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
        });
    };

    $scope.getLogs = function(){

      upgrade.getLogs($scope.upgradeObject,function(successResponse){
          $scope.updateOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));

          if((successResponse.data.indexOf("Stream :: close :: code: 0, signal: undefined")>-1 || successResponse.data.indexOf("OZONE_PROGRAM_COMPLETED")>-1)){
            $scope.refreshLog = false
            $scope.UpgradeButtonIcon = '';
          }else{
            $scope.UpgradeButtonIcon = 'refresh';
            $scope.refreshLog = true
          }

        },
        function(errorResponse){
          console.log("successResponse ="+ JSON.stringify(errorResponse.data))
        })
    };

    $scope.refreshLogs = function(){

      $scope.getLogs();
      var timer = $timeout(
        function(){
          //$scope.getLogs(tile);
          if($scope.refreshLog) {
            $scope.refreshLogs();
          }
        },
        5000
      );

      $scope.$on(
        "$destroy",
        function( event ) {
          $timeout.cancel( timer );
        }
      );

    };

    $scope.upgradeApplication = function(ev){

      $scope.UpgradeButtonIcon = 'refresh';

      upgrade.create(
        function(successResponse){
          $scope.refreshLog = true;
          $scope.upgradeObject = successResponse.data;
          $scope.UpgradeButtonTheme = 'green';

          var matches = $scope.upgradeObject.logfile.match(/.*_(.*).log/);
          if(matches.length > 1)$scope.logtime = matches[1];

          setTimeout(function(){
            $scope.refreshLogs();
          },2000);


        },
        function(errorResponse){
          $scope.UpgradeButtonIcon = 'error';
          $scope.UpgradeButtonTheme = 'red';
          $scope.errmsg = errorResponse.data;
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
        });

    };

    $scope.checkUpdates = function(){
      $scope.checkUpdatesButtonIcon = 'refresh';
      upgrade.checkUpdates(function(successResponse){

        $scope.checkUpdatesButtonIcon = 'check';
        $scope.updateOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));

      },function(errorResponse){
        $scope.checkUpdatesButtonIcon = 'error';
        console.log("Error Response" + errorResponse.data);
      })
    };

    $scope.getUpgradeInfo();

  }
}

angular.module('ehcOzoneApp')
  .component('upgrade', {
    templateUrl: 'app/admin/upgrade/upgrade.html',
    controller: UpgradeComponent
  });

})();
