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
  .directive('logViewer', function ($mdDialog) {
    return {
      templateUrl: 'app/directives/log_viewer/log_viewer.html',
      restrict: 'EA',
      scope: {
        tile : '=',
        getLogsService: '&',
        jobObjects: '='
      },
      link: function (scope, element, attrs) {

        scope.showLogDialog = function(ev) {

          $mdDialog.show({
            controller: DialogController,
            templateUrl: '/app/directives/log_viewer/log_console.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            locals: {
              tile: scope.tile,
              getLogsService: scope.getLogsService,
              jobObjects: scope.jobObjects
            },
          });
        };

        scope.tile.showLogDialog = scope.showLogDialog;

        function DialogController($scope, $mdDialog, $sce, ansi2html, tile, jobObjects, getLogsService) {

          $scope.logContent = null;
          $scope.tile = tile;
          $scope.jobObjects = jobObjects;
          $scope.selectedJob = {
            job : tile.configureObject
          };

          $scope.view = 'console';
          $scope.ansibleOutput = false;

          if(tile.configureObject && tile.configureObject.execType == 'Ansible'){
            $scope.ansibleOutput = true;
            $scope.view = 'table';
            $scope.$watch('tile.logContent',function(newValue){
              //$scope.logContent = $sce.trustAsHtml(ansi2html.toHtml(newValue).replace(/\n/g, "<br>"))
              $scope.processAnsibleOutput(newValue)

            });
          }


          /**
           * Show Logs
           */
          $scope.showLogs = function(){


            getLogsService()($scope.selectedJob.job,
              function(response){
                $scope.logContent = $sce.trustAsHtml(ansi2html.toHtml(response.data).replace(/\n/g, "<br>"))
            },function(response){

            })
          };




          /**
           * Process Ansible Output
           * @param ansibleOutput
           */
          $scope.processAnsibleOutput = function(ansibleOutput){

            $scope.ansibleOutputResult = [];
            $scope.ansibleOutputObject = {
              'plays' : [],
              'stats' : {}

            };
            //var re = /(.*{[^]+}.*)/g;
            var re = /--------BEGIN--------([^]+?)--------END--------/gm;
            var m;

            while ((m = re.exec(ansibleOutput)) !== null) {
              if (m.index === re.lastIndex) {
                re.lastIndex++;
              }
              // View your result using the m-variable.
              // eg m[0] etc.

              try{
                //$scope.ansibleOutputObject = JSON.parse(m[1]);
                var resultItem = JSON.parse(m[1].replace(/\r\n/g,""));
                if('play' in resultItem){
                  $scope.ansibleOutputObject.plays.push(resultItem);
                } else if('task' in resultItem){

                  var current_play = $scope.ansibleOutputObject.plays[$scope.ansibleOutputObject.plays.length-1];
                  var newTask = true;
                  angular.forEach(current_play.tasks, (task, index)=>{
                    if(task.task.id === resultItem.task.id){
                      newTask = false;
                      current_play.tasks[index] = resultItem
                    }
                  });


                  if(newTask)
                    current_play.tasks.push(resultItem);

                } else if('stats' in resultItem){
                  $scope.stats = resultItem.stats;
                }

              }catch(e){
                console.log("Error parsing ansible output" + e);
              }

            }


            $scope.ansibleOutputObject = serializeOutput($scope.ansibleOutputObject);

          };


          /**
           * Serialize Output
           * @param ansibleOutputObject
           * @returns {Array}
           */
          var serializeOutput = function(ansibleOutputObject){

            var result = [];
            angular.forEach(ansibleOutputObject.plays, playObject => {
              angular.forEach(playObject.tasks, taskObject => {
                angular.forEach(taskObject.hosts, (hostObject,hostName) => {

                  result.push({
                    icon:'keyboard_arrow_right',
                    playName: playObject.play.name,
                    taskName: taskObject.task.name,
                    hostName: hostName,
                    method: hostObject.invocation && hostObject.invocation.module_name,
                    changed: hostObject.changed,
                    skipped: hostObject.skipped,
                    hostObject: hostObject
                  })

                })
              })
            });

            return result;

          };

          $scope.expandRow = function(taskObject){
            taskObject.icon = taskObject.icon == 'keyboard_arrow_down' ? 'keyboard_arrow_right' : 'keyboard_arrow_down';
            taskObject.showLogs = !taskObject.showLogs
          };

          $scope.hide = function() {
            $mdDialog.hide();
          };

          $scope.cancel = function() {
            $mdDialog.cancel();
          };

          $scope.answer = function(answer) {
            $mdDialog.hide(answer);
          };
        }

      }
    };
  });
