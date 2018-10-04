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
(function () {

  class RunsComponent {
    constructor($scope, $stateParams, $sce, ansi2html, ansible, projects, $timeout, $mdDialog, toasts, log, time, Auth) {
      var component = $stateParams.component;
      $scope.component = component;

      $scope.logContent = null;
      $scope.dataLoaded = false;

      $scope.view = 'table';
      $scope.icon = 'list';
      $scope.ansibleOutput = false;
      $scope.progress = 0;
      $scope.vRALogs = null;

      $scope.tasksList = null;

      $scope.execution_duration = {
        days: null,
        hours: null,
        minuntes: null,
        seconds: null
      };

      var editor = null;

      $scope.isSuperAdmin = Auth.hasRole('superadmin');

      //To fix a warning message in console
      $scope.aceLoaded = function (_editor) {
        _editor.$blockScrolling = Infinity;
        editor = _editor;
        //_editor.gotoLine(100);
      };

      //Scroll to bottom of log messages always
      $scope.codeChanged = function (e) {
        $timeout(function () {
          e[1].scrollToLine(e[0].lines.length, true, true);
        }, 500);
      };

      /**
       * Get Ansible Jobs
       */
      $scope.getAnsibleJobRuns = function () {

        if ($scope.timer) $timeout.cancel($scope.timer);

        $scope.tasksList = null;
        $scope.execution_duration_days = null;

        if (!projects.selectedProject)return;
        $scope.dataLoaded = true;

        $scope.loading = true;
        ansible.get(projects.selectedProject._id, component, function (successResponse) {
            $scope.loading = false;
            $scope.jobObject = successResponse.data[successResponse.data.length - 1];
            $scope.jobObjects = successResponse.data;

            $scope.lastJobSelected = true;
            $scope.showRunTime = true;

            if ($scope.jobObject && $scope.jobObject.logfile) {
              var matches = $scope.jobObject.logfile.match(/.*_(.*).log/);
              if (matches.length > 1) $scope.logtime = matches[1];
            }

            if ($scope.jobObject && $scope.jobObject.state == 'active') getTimeDifference();
            //if ($scope.jobObject) getTimeDifference();

            if ($scope.jobObject && $scope.jobObject.state == 'stopping') $scope.stopButtonIcon = 'refresh';
            //showJobResults();

            $scope.selectedJob = {
              job: $scope.jobObject
            };

            refreshJobData();

          },
          function (errorResponse) {
            $scope.loading = false;
            $scope.buttonText = 'Run';
            console.log("errorResponse =" + JSON.stringify(errorResponse.data))
          });

      };

      /**
       * Refresh Job Data
       * Get Job execution results
       */
      var refreshJobData = function () {

        if (!($scope.jobObject && $scope.jobObject._id))return;

        // Get Rollback points
        ansible.getRollbackPoints({project: projects.selectedProject},
          function(response){
            console.log(response.data);
            $scope.rollbackPoints = response.data;
          }, function(response){
            console.error(response.data)
          });

        ansible.show($scope.jobObject._id,
          function (response) {
            $scope.jobObject = response.data;
            showJobResults()
          }, function (response) {
            setTimerForJobRefresh();
            toasts.showError(response.data, 'Error', 'red');
            console.log(response.data)
          })

      };

      /**
       * Get Time Difference
       * If duration exists in job, meaning the job has finished , then use duration to display time
       * Else if job is running calculate difference from job start time
       */
      var getTimeDifference = function () {

        if ($scope.jobObject.duration) $scope.timeDifference = $scope.jobObject.duration;
        else $scope.timeDifference = new Date() - new Date($scope.jobObject.date);

        $scope.execution_duration = time.getTimeDifference($scope.timeDifference)

      };


      /**
       * Show Job Results
       */
      var showJobResults = function () {
        if ($scope.jobObject) {

          //log.refreshLogs($scope,$scope,ansible.getLogs);
          ansible.getLogs($scope.jobObject,
            function (successResponse) {
              if (typeof successResponse.data == 'object')
                successResponse.data = successResponse.data.join("\n");
              $scope.logContent = successResponse.data;

              $scope.displayLogContent = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));

              if ($scope.jobObject && $scope.jobObject.execType == 'Ansible') {
                $scope.ansibleOutput = true;
                processLogContent($scope.logContent);
              }

              setTimerForJobRefresh();

            }, function (errorResponse) {
              console.log("Error - " + errorResponse.data);
              toasts.showError(errorResponse.data, 'Error', 'red');
            })
        }
      };


      /**
       *
       * @param newValue
       */
      var processLogContent = function (newValue) {
        //$scope.logContent = $sce.trustAsHtml(ansi2html.toHtml(newValue).replace(/\n/g, "<br>"))
        if (newValue) {
          if (typeof newValue == 'object')
            newValue = newValue.join("\n");

          $scope.ansibleOutputObject = {
            'plays': [],
            'stats': {}
          };

          //Only get tasks list (all jobs to run) the first time.
          //Then only refresh the logs
          if (!$scope.tasksList) {
              $scope.tasksList = $scope.jobObject.ansibleTasksToExecute;
              //$scope.uniquePlaysList = getUniquePlays($scope.tasksList)
              getUniquePlays();
          }


          try {
            $scope.logJSONContent = JSON.stringify($scope.jobObject.ansibleResults, null, "\t");
          } catch (ex) {
            $scope.logJSONContent = ex
          }


          $scope.ansibleOutputObject = {
            'plays': $scope.jobObject.ansibleResults,
            'stats': $scope.jobObject.ansibleStats
          };
          $scope.stats = $scope.jobObject.ansibleStats;

          serializeOutput($scope.ansibleOutputObject, $scope.jobObject.ansibleStats);
          mapResultsToPlaysToRun();

          $scope.filteredTasks = $scope.tasksList.slice(0, 10);

          $scope.execution_duration = {};

          if ($scope.jobObject.state == 'active' || $scope.jobObject.state == 'stopping') getTimeDifference();

          if ($scope.jobObject.state == 'stopping') $scope.stopButtonIcon = 'refresh';

          if (newValue.indexOf('Playbook run took') > -1) {
            //Get Time it took to run
            var runtime_re = /[^]+Playbook run took(.*)[^]+/g;
            var execution_duration = newValue.replace(runtime_re, '$1');

            if (execution_duration) {
              $scope.execution_duration.days = execution_duration.replace(/(.*) days, (.*) hours, (.*) minutes, (.*) seconds/, "$1");
              $scope.execution_duration.hours = execution_duration.replace(/(.*) days, (.*) hours, (.*) minutes, (.*) seconds/, "$2");
              $scope.execution_duration.minutes = execution_duration.replace(/(.*) days, (.*) hours, (.*) minutes, (.*) seconds/, "$3");
              // $scope.execution_duration_seconds = execution_duration.replace(/(.*) days, (.*) hours, (.*) minutes, (.*) seconds/,"$4");
              $scope.execution_duration.seconds = execution_duration.replace(/(.*) days, (.*) hours, (.*) minutes, (.*) seconds/, "$4");
              if ($scope.execution_duration.seconds > 60) $scope.execution_duration.seconds = 0;
            }
          }

        }

      };

      /**
       * Set Timer for Job Refresh
       */
      var setTimerForJobRefresh = function () {

        if ($scope.jobObject && $scope.jobObject.state == 'active' || $scope.jobObject.state == 'stopping') {
          $scope.timer = $timeout(function () {
            refreshJobData()
          }, 10000);

          if ($scope) {
            $scope.$on(
              "$destroy",
              function (event) {
                $timeout.cancel($scope.timer);
              }
            );
          }
        }

      };

      /**
       * On a run selected
       */
      $scope.runSelected = function () {
        $scope.tasksList = null;
        $scope.jobObject = $scope.selectedJob.job;

        // Check if its the last run
        $scope.lastJobSelected = false;
        var lastJob = $scope.jobObjects[$scope.jobObjects.length - 1];
        if(lastJob._id == $scope.jobObject._id){
          $scope.lastJobSelected = true
        }

        // This is a workaround to update top timer. Without this, when job selection changes it does not get updated.
        $scope.showRunTime = false;
        $timeout(function () {
          $scope.showRunTime = true;
          $scope.$apply();
        }, 1000);

        refreshJobData();
      };


      $scope.stopButtonIcon = 'stop';
      /**
       * Show Stop Confirm
       * @param ev
       */
      $scope.stopJob = function (ev) {
        // Appending dialog to document.body to cover sidenav in docs app
        var confirm = $mdDialog.confirm()
          .title('Confirm')
          .textContent('Are you sure you want to stop the workflow execution? The job will finish after the current task is complete')
          .ariaLabel('Stop')
          .targetEvent(ev)
          .ok('Yes')
          .cancel('No');
        $mdDialog.show(confirm).then(function () {
          $scope.stopButtonIcon = 'refresh';

          ansible.stopAnsiblePlayBookExecution({_id: $scope.jobObject._id}, function (response) {
            //$scope.stopButtonIcon = 'done';
            console.log("Stop Job " + response);
            $scope.jobObject = response.data;
            //refreshJobData()
          }, function (response) {
            $scope.stopButtonIcon = 'error';
            console.log("Stop Job Error " + response);
            toasts.showError(response.data, 'Error', 'red');
          });
        }, function () {
          // Dialogue Cancel Action
        });
      };

      $scope.killButtonIcon = 'cancel';
      /**
       * Show Kill Confirm
       * @param ev
       */
      $scope.killJob = function (ev) {
        // Appending dialog to document.body to cover sidenav in docs app
        var confirm = $mdDialog.confirm()
          .title('Kill Job?')
          .textContent('Are you sure you want to kill the workflow execution? This process will be terminated but any remote processes initiated by this process may still be running.')
          .ariaLabel('Kill')
          .targetEvent(ev)
          .ok('Yes')
          .cancel('No');
        $mdDialog.show(confirm).then(function () {
          $scope.killButtonIcon = 'refresh';

          ansible.killAnsiblePlayBookExecution({_id: $scope.jobObject._id},
            function(response){
              $scope.jobObject = response.data;
            }, function(errorResponse){
              $scope.killButtonIcon = 'error';
              toasts.showError(errorResponse.data, 'Error', 'red');
              console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
            })

        }, function () {
          // Dialogue Cancel Action
        });
      };


      /**
       * Replace _dot_ and _dollar_ from key with . and $
       * The Ansible callback plugin replaces . and $ with _dot_ and _dollar_ before updating results in database as MongoDB doesnt like . or $ in database
       * Here we are converting it back during display. Only doing this for host names.
       * @param key
       */
      var replaceDotInKey = function (key) {
        try {
          if (typeof key == "object") key = JSON.stringify(key);
          return key && key.replace(/_dot_/g, ".").replace(/_dollar_/g, "$")
        } catch (e) {
          console.log("Unable to replace dot in key " + key);
          return key
        }

      };

      /**
       * Serialize Output
       * @param ansibleOutputObject
       * @param stats
       * @returns {Array}
       */
      var serializeOutput = function (ansibleOutputObject, stats) {

        var lastRunningTask;
        $scope.showVraLogs = false;
        angular.forEach(ansibleOutputObject.plays, playObject => {
          playObject.resultTasks = [];
          playObject.expand = playObject.expand || {value: false};
          playObject.icon = 'keyboard_arrow_right';
          calculateTaskExecutionDuration(playObject)

          angular.forEach(playObject.tasks, taskObject => {
            var subTasks = [];
            var subTaskObject;
            var overallTaskStatus = taskObject.status;
            var overallExpandIcon = 'keyboard_arrow_right';
            var overallExpandState = {value: false};
            //If no hosts then it means task is running

            if (!taskObject.hosts || angular.equals({}, taskObject.hosts)) {
              subTaskObject = {
                icon: 'keyboard_arrow_right',
                playName: playObject.play.name,
                taskName: taskObject.task.name,
                status: taskObject.status
              };

              // Special treatment for vRA to show Installation Logs
              if (subTaskObject && (taskObject.status == "Running" || taskObject.status == "Failed") && taskObject.task.name && (taskObject.task.name.indexOf('vRA Installation Wizard') > -1 )) {
                subTaskObject.showVraLogs = true;
                taskObject.showVraLogs = true;
              }

              overallTaskStatus = taskObject.task.status;
              subTasks.push(subTaskObject);

            }


            angular.forEach(taskObject.hosts, (hostObject, hostName) => {

              calculateTaskExecutionDuration(hostObject);

              var results = hostObject.results || [hostObject];

              angular.forEach(results, result => {

                var _hostName = hostName;
                if (result.item && typeof result.item == "string" || typeof result.item == "number") _hostName = hostName + "->" + result.item;

                try {
                  if (result.item && typeof result.item == "object") {

                    var resultItem = result.item;

                    if (Array.isArray(resultItem)) resultItem = resultItem[0];

                    if ('key' in resultItem) _hostName = hostName + " --> " + resultItem.key;
                    else if ('FQDN' in resultItem) _hostName = hostName + " --> " + resultItem.FQDN;
                    else if ('name' in resultItem) _hostName = hostName + " --> " + resultItem.name;
                    else if ('hostName' in resultItem) _hostName = hostName + " --> " + resultItem.hostName;
                    else _hostName = hostName + " --> " + Object.values(resultItem).join(",");
                  }
                } catch (e) {
                  console.error("Unable to find hostName- " + e)
                }


                subTaskObject = {
                  playName: playObject.play.name,
                  taskName: taskObject.task.name,
                  hostName: replaceDotInKey(_hostName),
                  method: result.invocation && result.invocation.module_name,
                  changed: result.changed,
                  skipped: result.skipped,
                  hostObject: result,
                  hasMsg: (result.stdout || result.msg || result.item || result.stderr || result.module_stderr || (result.warnings && result.warnings.length)),
                  status: result.status,
                  icon: 'keyboard_arrow_right',
                  expand: {value: false}
                };

                // Special treatment for vRA to show Installation Logs
                if (subTaskObject && (taskObject.status == "Running" || taskObject.status == "Failed") && taskObject.task.name && (taskObject.task.name.indexOf('vRA Installation Wizard') > -1 )) {

                  subTaskObject.showVraLogs = true;
                  taskObject.showVraLogs = true;
                }

                if (result.msg && result.msg.data) {
                  try {
                    result.dataJsonString = JSON.stringify(JSON.parse(result.msg.data), null, "\t");
                    result.dataJsonHeight = result.dataJsonString.split("\n").length * 18;

                    if (result.dataJsonHeight > 500) {
                      result.dataJsonHeight = 500
                    }

                  } catch (e) {
                    result.dataJsonString = result.msg.data;
                    result.dataJsonHeight = 100
                  }
                } else if (result.item) {
                  result.dataJsonString = JSON.stringify(result.item, null, "\t");

                  if (result.msg) {
                    result.dataJsonString += "\n" + JSON.stringify({"Message": result.msg}, "\t");
                  }

                  result.dataJsonHeight = result.dataJsonString.split("\n").length * 18;
                }

                subTasks.push(subTaskObject)
              });
            });

            if (taskObject.task.name) $scope.lastRunningTaskIndex = 0;

            // Map pre-defined tasks list with results of execution
            angular.forEach($scope.tasksList, (task, index) => {
              if (task.taskName === taskObject.task.name && task.playName === playObject.play.name) {
                lastRunningTask = task;
                $scope.lastRunningTaskIndex = index;
                task.subTasks = subTasks;
                task.status = overallTaskStatus;
                playObject.status = overallTaskStatus;
                if (!task.icon) task.icon = overallExpandIcon;
                if (!task.expand) task.expand = overallExpandState;
                playObject.resultTasks.push(task);
              }

            });

          })
        });

        // If stats exist then job is finished, mark all pending tasks as not run
        if (stats || ($scope.jobObject.state != 'active' && $scope.jobObject.state != 'stopping')) {
          markRunningTasksOnFinish($scope.tasksList);
        }

        $scope.progressType = "info";

        //return subTasks;
        //$scope.tasksList[$scope.tasksList.length-1].status = 'RUNNING'
        var total_number_tasks = $scope.tasksList && $scope.tasksList.length || 0;
        if (!(stats || ($scope.jobObject.state != 'active' && $scope.jobObject.state != 'stopping')) && lastRunningTask) {
          // lastRunningTask.status = "RUNNING";
          total_number_tasks += 1;
        }

        if ($scope.jobObject.state == 'failed' || $scope.jobObject.state == 'stopped') $scope.progressType = "danger";
        if ($scope.jobObject.state == 'complete') $scope.progressType = "success";

        if ($scope.lastRunningTaskIndex > -1 && total_number_tasks > 0) {

          $scope.progress = Math.round(($scope.lastRunningTaskIndex + 1) / total_number_tasks * 100);

          if (total_number_tasks == 1 && $scope.jobObject.state == 'active' && !($scope.progress > 0)) {
            $scope.progress = 0
          }

        }

      };

      projects.subscribeCustom($scope, $scope.getAnsibleJobRuns);

      if (!$scope.dataLoaded) {
        $scope.getAnsibleJobRuns()
      }

      ansible.showAgentLogsPopup();

      /**
       * Mark Running Tasks on Finish
       * @param tasksList
       */
      var markRunningTasksOnFinish = function(tasksList){
        tasksList && angular.forEach(tasksList, function (task) {
          markRunningTasksOnFinish(task.subTasks);

          if(!task.status) return;
          if (task.status.toLowerCase() === 'queued') {
            task.status = 'NOT RUN'
          } else if (task.status.toLowerCase() === 'running') {
            task.status = 'UNKNOWN'
          } else if (task.status.toLowerCase() === 'loading') {
            task.status = 'UNKNOWN'
          }

        });


        $scope.uniquePlays && angular.forEach($scope.uniquePlays, (play, index) => {

          if(!play.status) return;
          if (play.status.toLowerCase() === 'queued') {
            task.status = 'NOT RUN'
          } else if (play.status.toLowerCase() === 'running') {
            play.status = 'UNKNOWN'
          } else if (play.status.toLowerCase() === 'loading') {
            play.status = 'UNKNOWN'
          }

        });

      };

      //projects.refresh();

      /**
       * Show vRA Logs
       */
      $scope.displayVraLogs = function(){
        log.openMoreInfo(false, 'Fetching vRA Logs....', 'vRA Logs', 'blue');
      };

      /**
       * Calculate Task Execution Duration
       */
      var calculateTaskExecutionDuration = function (hostObject) {
        try {
          if (hostObject.start_time) {
            if (hostObject.end_time) {
              hostObject.execution_duration = time.getTimeDifference(hostObject.end_time - hostObject.start_time)
            } else {
              hostObject.execution_duration = time.getTimeDifference(Date.now() - hostObject.start_time)
            }
          }
        } catch (e) {
          console.error("Exception calculating task execution time duration")
        }

      };

      /**
       * Get Unique Plays
       */
      var getUniquePlays = function(ansibleTasksToExecute){
        $scope.uniquePlays = [];
        $scope.tempuniquePlays = [];
        $scope.jobObject.ansibleTasksToExecute.map(task => {
          $scope.tempuniquePlays.indexOf(task.playName) < 0 && $scope.uniquePlays.push({
            name: task.playName,
            icon: 'keyboard_arrow_right',
            expand: {value: false}
          }) && $scope.tempuniquePlays.push(task.playName)
        })
      };


      /**
       * Map Results to List of Plays to run
       */
      var mapResultsToPlaysToRun = function(){
        // Map pre-defined tasks list with results of execution
        angular.forEach($scope.uniquePlays, (play, index) => {
          angular.forEach($scope.ansibleOutputObject.plays, playbObj =>{
            if (play.name === playbObj.play.name) {
              play.status = playbObj.status;
              play.execution_duration = playbObj.execution_duration;
              play.resultTasks = playbObj.resultTasks;
            }

          });

        });

        // If stats exist then job is finished, mark all pending tasks as not run
        if ($scope.jobObject.state != 'active' && $scope.jobObject.state != 'stopping') {
          markRunningTasksOnFinish($scope.tasksList);
        }

      }

    }
  }

  angular.module('ehcOzoneApp')
    .component('runs', {
      templateUrl: 'app/ansible/runs/runs.html',
      controller: RunsComponent
    });

})();
