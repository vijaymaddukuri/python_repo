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
  .controller('RevertAllCtrl', function ($scope,$mdDialog,snapshots) {

    $scope.snapshots = snapshots;
    $scope.filterSnapshot = {name:''};
    $scope.selectedSnapshots = [];

    $scope.cancel = function() {
      $mdDialog.cancel();
    };

    $scope.revertAll = function() {

      var countDict = {};
      var all_good = true;

      var selectedSnapshotsResult = [];

      angular.forEach($scope.selectedSnapshots, selectedSnapshot => {
        if(!countDict[selectedSnapshot.component_name])countDict[selectedSnapshot.component_name] = 0;
        countDict[selectedSnapshot.component_name] += 1;

        if(countDict[selectedSnapshot.component_name] > 1){
          $scope.err_msg = "Two entries selected for the same VM - " + selectedSnapshot.component_name;
          all_good = false;
        }

      });

      if(all_good)$mdDialog.hide($scope.selectedSnapshots);
    };


  });
