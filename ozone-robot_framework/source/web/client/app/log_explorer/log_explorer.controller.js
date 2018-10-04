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

class LogExplorerComponent {
  constructor($scope, logExplorer, configure) {

    $scope.allLogFiles = [];
    $scope.showProgressbar = true;

    logExplorer.getFilesList(function(response){
        $scope.showProgressbar = false;
        categorize(response.data)
      },
      function(response){
        $scope.showProgressbar = false;
        console.log(response)
      });



    var categorize = function(logList){
      $scope.allLogFiles = [];
      angular.forEach(logList, logFile => {
        if(logFile.indexOf("\\") > -1){
          $scope.allLogFiles.push({category:logFile.split("\\")[0],fileName:logFile.split("\\")[1],filePath:logFile})
        }else{
          $scope.allLogFiles.push({category:'default',fileName:logFile,filePath:logFile})
        }

      });
    };

    $scope.showLogFile = function(filePath){

      console.log("FilePath = " + filePath);

      if(filePath == 'fehc.log'){

        $scope.showProgressbar = true;
        logExplorer.getLogs('agent', 20000, function (response) {
          $scope.showProgressbar = false;
          $scope.logContent = response.data;
        }, function(response){
          $scope.showProgressbar = false;
          $scope.logContent = response.data;
        });
      }else{
        $scope.showProgressbar = true;
        logExplorer.getFile(filePath, function(response){
          $scope.showProgressbar = false;
          $scope.logContent = response.data;
        },function(response){
          $scope.showProgressbar = false;
          $scope.logContent = response.data
        })
      }



    }

  }
}

angular.module('ehcOzoneApp')
  .component('logExplorer', {
    templateUrl: 'app/log_explorer/log_explorer.html',
    controller: LogExplorerComponent
  });

})();
