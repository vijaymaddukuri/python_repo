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

  class RunComponent {
    constructor($scope, $mdDialog, $stateParams, ansible, projects, $location, $timeout, $window, toasts, Auth) {

      var component = $stateParams.component;
      var masterComponent = $stateParams.masterComponent;
      var ansibleJobId = $stateParams.ansibleJobId;
      $scope.retryFailed = $stateParams.retryFailed;
      $scope.rerun = ansibleJobId && true || false;
      var restoreState = $stateParams.restoreState;

      $scope.lastSelectOperation = null;
      $scope.lastSelectIndex = null;

      $scope.isSuperAdmin = Auth.hasRole('superadmin');

      $scope.dataLoaded = false;
      $scope.playbuttonTheme = 'md-raised';
      $scope.taskListButtonTheme = '';

      $scope.query = {
        order: 'name',
        limit: 5,
        page: 1
      };

      $scope.sortableOptions = {
        dropzone: '<tr md-row><td style="background:lightgrey;align-content: center;text-align: center; color:whitesmoke;" colspan="3" md-cell>Drop</td></tr>'
      };

      $scope.preventDrag = function (event) {
        event.stopPropagation();
      };

      var loadingTaskButtonText = {
        default: 'Get Task List',
        progress: 'Getting Task List',
        completed: 'Execute'
      };

      var executeTaskButtonText = {
        default: 'Run',
        progress: 'Running',
        completed: 'Success'
      };

      $scope.playButtonText = executeTaskButtonText;
      $scope.taskListButtonText = loadingTaskButtonText;

      $scope.playButton = {
        state: 'default'
      };

      $scope.taskListButton = {
        state: 'default'
      };

      $scope.additional_options = {
        check_mode: 'No_Check',
        verbose: 'verbose',
        verbose_detail: '',
        pre_validation: false,
        post_validation: false,
        advanced_options: false
      };


      $scope.toolTipMsg = '';

      $scope.additional_tags = {show: false};

      $scope.component = component;
      $scope.component_list = component && component.split(",");
      $scope.selectedWorkflows = angular.copy($scope.component_list);

      // Check for restore workflow
      $scope.isRollbackWorkflow = false;

      angular.forEach($scope.component_list, component => {
        if (component.indexOf('_rollback') == 0 || component.indexOf('_reset-ehc-environment') == 0) {
          $scope.isRollbackWorkflow = true;

        }
      });


      /**
       * Reset all Lists
       */
      var resetAllLists = function () {
        $scope.tagsList = [];
        $scope.tasksList = [];
        $scope.selectedTask = [];
        $scope.selectedTags = [];
        $scope.selectedHosts = [];

        $scope.all_tags = [];
        $scope.all_hosts = [];
        filterTasks();
      };

      /**
       * Show Confirm Modal. While Re-Executing Jobs
       * @param ev
       * @param tile
       */
      $scope.showConfirm = function (ev, tile) {
        // Appending dialog to document.body to cover sidenav in docs app
        var confirm = $mdDialog.confirm()
          .title('Re-run')
          .textContent('Are you sure you want to re-run?')
          .ariaLabel('Reconfigure')
          .targetEvent(ev)
          .ok('Yes')
          .cancel('No');
        $mdDialog.show(confirm).then(function () {
          $scope.ansibleObject(ev, tile, false);
        }, function () {

        });
      };

      /**
       * Configure Object
       * @param ev
       * @param tile
       * @param showConfirm
       * @param ansibleData
       */
      $scope.ansibleObject = function (ev, tile, showConfirm, ansibleData) {

        if (showConfirm != false) {
          return $scope.showConfirm(ev, tile)
        }

        $scope.buttonicon = 'refresh';
        $scope.playButton.state = 'RUNNING';
        ansible.executeAnsiblePlayBook(ansibleData,
          function (successResponse) {
            // On success wait for 3 seconds and move to results window
            $scope.moveToResultsTimeout = $timeout(function () {
              $location.path("/ansible/runs/" + component);
            }, 3000);

            // On scope destroy cancel timeout
            $scope.$on('$destroy', function () {
              // Make sure that the timer is destroyed
              $timeout.cancel($scope.moveToResultsTimeout);
            });

          },
          function (errorResponse) {
            $scope.refreshLog = false;

            $scope.state = 'FAIL';
            $scope.toolTipMsg = errorResponse.data;
            toasts.showError(errorResponse.data.error || errorResponse.data, 'Error', 'red');

            $scope.playButton.state = 'FAIL';

            if ($scope.logRefreshTimer) {
              $timeout.cancel($scope.logRefreshTimer);
            }
            $scope.logOutput = errorResponse.data;
            $scope.logsAvailable = true;
            $scope.showLog = true;
          });

      };


      /**
       * Execute Playbook
       */
      $scope.executePlaybook = function (ev) {

        $scope.playButton.state = 'RUNNING';

        var filteredOrderedWorkflows = $scope.component_list.filter(component => {
          return $scope.selectedWorkflows.indexOf(component) > -1
        });

        $scope.AnsiblePlayBookLoading = true;
        var reqBody = {
          type: (masterComponent || filteredOrderedWorkflows),
          refid: projects.selectedProject._id + "_" + filteredOrderedWorkflows.join(',').replace(/,/g, '__'),
          project: projects.selectedProject
        };

        if ($scope.isRollbackWorkflow) {
          reqBody.extra_vars = {
            'EHC_REVERT_TO_STATE': $scope.lastRollbackPoint
          }
        }

        reqBody.tags = [];

        $scope.selectedTags.map(tag => {
          if (tag.name)
            reqBody.tags.push(tag.name.trim())
        });

        reqBody.limit_to_hosts = [];

        $scope.selectedHosts.map(host => {
          if (host.name)
            reqBody.limit_to_hosts.push(host.name.trim())
        });

        reqBody.verbose = $scope.additional_options.verbose_detail || $scope.additional_options.verbose;
        reqBody.check_mode = $scope.additional_options.check_mode;
        $scope.result = "Running...";

        $scope.ansibleObject(ev, component, false, reqBody);
      };

      /**
       * Drag Ended Event - Used when dragging/reordering playbook.
       * Feature May be disabled currently.
       * @param element
       * @param newIndex
       * @param oldIndex
       * @param sequence
       */
      $scope.dragEnded = function (element, newIndex, oldIndex, sequence) {

        if (newIndex !== oldIndex) {
          $scope.mergeAndGetTasksList();
        }

      };


      var lastRefershTime = null;
      /**
       * Handle multi selection event fired from the UI
       * Only run getTasksList once
       */
      $scope.mergeAndGetTasksList = function ($event) {

        resetAllLists();

        $scope.filteredOrderedWorkflows = $scope.component_list && $scope.component_list.filter(component => {
          return $scope.selectedWorkflows.indexOf(component) > -1
        });

        if (!($scope.filteredOrderedWorkflows && $scope.filteredOrderedWorkflows.length))return;

        var currentTime = new Date().getTime();

        if (lastRefershTime == null || (currentTime - lastRefershTime) > 500) {
          lastRefershTime = new Date().getTime();
          $timeout(function () {
            $scope.getAnsibleTasksList();
            lastRefershTime = null;
          }, 500)
        }

      };

      /**
       * Get Ansible Tasks List
       * Get list of ansible tasks and display table
       * Get Unique list of tags
       * Get Unique list of hosts
       *
       */
      $scope.getAnsibleTasksList = function () {

        if (!projects.selectedProject)return;

        if (!($scope.filteredOrderedWorkflows && $scope.filteredOrderedWorkflows.length))return;

        // If Restore/Rollback workflow get List of Rollback Points and get last rollback point
        if ($scope.isRollbackWorkflow) {
          ansible.getRollbackPoints({project: projects.selectedProject},
            function (response) {
              console.log(response.data);
              $scope.rollbackPoints = response.data;
              $scope.lastRollbackPoint = $scope.rollbackPoints.length && $scope.rollbackPoints.slice(-1)[0].rollback_point;
            }, function (response) {
              console.error(response.data)
            });
        }

        var ansibleData = {
          type: $scope.filteredOrderedWorkflows,
          refid: projects.selectedProject._id + "_" + $scope.filteredOrderedWorkflows.join('__').replace(/,/g, '__'),
          project: projects.selectedProject

        };

        // if (restoreState) {
        //   ansibleData.extra_vars = {
        //     'EHC_REVERT_TO_STATE': $scope.lastRollbackPoint
        //   }
        // }

        if (!$scope.selectedWorkflows.length)return;

        $scope.taskListButton.state = 'RUNNING';
        $scope.taskListButtonTheme = '';


        ansible.getAnsibleTasksList(ansibleData,
          function (successResponse) {

            $scope.playbooksTaskList = successResponse.data;

            angular.forEach($scope.playbooksTaskList.playbooks, playbook => {
              angular.forEach(playbook.plays, play => {
                $scope.all_hosts = $scope.all_hosts.concat(play.hosts);
                $scope.all_tags = $scope.all_tags.concat(play.tags);
                angular.forEach(play.tasks, task => {
                  var task_name = task.name;
                  if (task_name && task_name.indexOf(":") > -1)
                    task_name = task_name.split(":")[1];
                  $scope.tasksList.push({
                    playbook: playbook.name,
                    play: play.name,
                    task: task_name,
                    tags: task.tags,
                    hosts: play.hosts
                  })
                  $scope.all_tags = $scope.all_tags.concat(task.tags);
                })
              })
            });

            // Get Unique List of tags
            $scope.all_tags = Array.from(new Set($scope.all_tags));

            // Get Unique List of hosts
            $scope.all_hosts = Array.from(new Set($scope.all_hosts));

            $scope.all_hosts = $scope.all_hosts.map(host => {
              return {name: host}
            });

            var skip_tags = ['pre_validation', 'post_validation'];

            $scope.all_tags = $scope.all_tags.map(tag => {
              return {name: tag}
            }).filter(tag => {
              return skip_tags.indexOf(tag.name) < 0;
            });

            //Select all tags by default
            // Assign index to each tag which will be used for multiple selection
            angular.forEach($scope.all_tags, (tag, index) => {
              tag.index = index;

              $scope.selectedTags.push(tag)
            });

            //Select all hosts by default
            angular.forEach($scope.all_hosts, (host, index) => {
              $scope.selectedHosts.push(host)
            });

            //Show all tasks by default
            $scope.filteredTasks = $scope.tasksList;
            $scope.filteredHosts = $scope.all_hosts;

            $scope.taskListButton.state = 'default';
            //$scope.playButtonText = executeTaskButtonText;
            $scope.taskListButtonTheme = '';

            filterPreviousTasks();
            // Re-run set previously selected tags
            if (ansibleJobId) {
              $scope.taskListButton.state = 'RUNNING';
              ansible.show(ansibleJobId,
                function (response) {
                  $scope.taskListButton.state = 'default';
                  $scope.jobObject = response.data;

                  //Update tag selection from previous run
                  if ($scope.jobObject.info && $scope.jobObject.info.tags) {
                    $scope.selectedTags = [];
                    angular.forEach($scope.jobObject.info.tags, previously_selected_tag => {
                      angular.forEach($scope.all_tags, current_tag => {
                        if (previously_selected_tag == current_tag.name) {
                          $scope.selectedTags.push(current_tag)
                        }
                      })
                    });
                    filterTasks();
                  }

                  //Update host selection from previous run
                  if ($scope.jobObject.info && $scope.jobObject.info.limit_to_hosts) {
                    $scope.selectedHosts = [];
                    angular.forEach($scope.jobObject.info.limit_to_hosts, previously_selected_host => {
                      angular.forEach($scope.filteredHosts, current_host => {
                        if (previously_selected_host == current_host.name) {
                          $scope.selectedHosts.push(current_host)
                        }
                      })

                    });
                    $scope.filterTasksByHosts();
                  }

                  if ($scope.retryFailed) {
                    filterTasksToRetry();
                    filterTasks();
                  }

                  $scope.taskListButtontoolTipMsg = '';

                }, function (errorResponse) {
                  $scope.taskListButton.state = 'FAIL';
                  console.log(errorResponse);
                  $scope.taskListButtontoolTipMsg = errorResponse.data;
                  toasts.showError(errorResponse.data, 'Error', 'red');

                })
            }

            //
            $scope.taskListButtontoolTipMsg = '';
        },
          function (errorResponse) {

            $scope.taskListButton.state = 'FAIL';
            $scope.taskListButtontoolTipMsg = errorResponse.data;
            toasts.showError(errorResponse.data, 'Error', 'red');

          });

      };


      /**
       * On deselecting a row
       * @param selectedItem
       */
      $scope.rowDeSelected = function (selectedItem) {
        if ($window.event && $window.event.shiftKey && $scope.lastSelectOperation) multiSelect(selectedItem.index);

        if (!($window.event && $window.event.shiftKey)) {
          $scope.lastSelectOperation = "Deselect";
          $scope.lastSelectIndex = selectedItem.index;
        }

        filterTasks();

      };

      /**
       * On Row Selected Filter Tasks and Hosts
       */
      $scope.rowSelected = function (selectedItem) {

        if ($window.event && $window.event.shiftKey && $scope.lastSelectOperation) multiSelect(selectedItem.index);

        if (!($window.event && $window.event.shiftKey)) {
          $scope.lastSelectOperation = "Select";
          $scope.lastSelectIndex = selectedItem.index;
        }

        filterTasks();
      };

      /**
       * Multi Select Algorithm
       * @param currentItemIndex
       */
      var multiSelect = function (currentItemIndex) {

        if ($window.event && $window.event.shiftKey && $scope.lastSelectOperation && angular.isDefined($scope.lastSelectIndex)) {

          if (currentItemIndex < $scope.lastSelectIndex) {
            var tempIndex = $scope.lastSelectIndex;
            $scope.lastSelectIndex = currentItemIndex;
            currentItemIndex = tempIndex
          }

          for (var i = $scope.lastSelectIndex; i <= currentItemIndex; i++) {
            var foundInSelected = false;
            for (var j = 0; j < $scope.selectedTags.length; j++) {
              if ($scope.all_tags[i] == $scope.selectedTags[j]) {
                foundInSelected = true;
                if ($scope.lastSelectOperation == "Deselect") {
                  $scope.selectedTags.splice(j, 1)
                }
              }
            }

            if (!foundInSelected && $scope.lastSelectOperation == "Select") {
              $scope.selectedTags.push($scope.all_tags[i]);
            }

          }

        }

      };


      /**
       * Filter Tasks to show only selected
       */
      var filterTasks = function () {

        if ($scope.additional_options.pre_validation) $scope.selectedTags = [{name: 'pre_validation'}];
        if ($scope.additional_options.post_validation) $scope.selectedTags = [{name: 'post_validation'}];

        $scope.filteredTasks = [];
        $scope.filteredHosts = [];
        angular.forEach($scope.tasksList, task => {
          var taskAdded = false;
          angular.forEach($scope.selectedTags, selectedTag => {
            if (!taskAdded && task.tags.indexOf(selectedTag.name) > -1) {
              $scope.filteredTasks.push(task);
              $scope.filteredHosts = $scope.filteredHosts.concat(task.hosts);
              taskAdded = true;
            }
          })
        });

        $scope.filteredHosts = Array.from(new Set($scope.filteredHosts));
        $scope.filteredHosts = $scope.filteredHosts.map(host => {
          return {name: host}
        });

        $scope.selectedHosts = [];
        //Select all hosts by default
        angular.forEach($scope.filteredHosts, (host, index) => {
          $scope.selectedHosts.push(host)
        });


      };


      /**
       * Filter Tasks to show only selected
       */
      $scope.filterTasksByHosts = function () {

        $scope.filteredTasks = [];
        //$scope.filteredHosts = [];
        angular.forEach($scope.tasksList, task => {
          var taskAdded = false;
          angular.forEach($scope.selectedTags, selectedTag => {
            angular.forEach($scope.selectedHosts, selectedHost => {
              if (!taskAdded && task.tags.indexOf(selectedTag.name) > -1 && task.hosts.indexOf(selectedHost.name) > -1) {
                $scope.filteredTasks.push(task);
                //$scope.filteredHosts = $scope.filteredHosts.concat(task.hosts);
                taskAdded = true;
              }
            });
          })
        });

      };

      /**
       * Filter Tasks to retry in case of "retryFailed"
       */
      var filterTasksToRetry = function () {

        var lastResult;
        var lastTask;
        if ($scope.jobObject.ansibleResults && $scope.jobObject.ansibleResults.length) {
          lastResult = $scope.jobObject.ansibleResults[$scope.jobObject.ansibleResults.length - 1]
        }

        if (lastResult && lastResult.tasks && lastResult.tasks.length) {
          lastTask = lastResult.tasks[lastResult.tasks.length - 1];
        }

        if (lastTask && lastTask.task && lastTask.task.name) {
          for (var i = 0; i < $scope.tasksList.length; i++) {
            var task = $scope.tasksList[i];

            if (task && task.task && lastTask.task && task.task.trim() === lastTask.task.name) {
              return
            }

            for (var index = 0; index < $scope.selectedTags.length; index++) {
              var selectedTag = $scope.selectedTags[index];
              for (var k = 0; k < task.tags.length; k++) {
                var tag = task.tags[k];
                if (tag === selectedTag.name && !isTagUsedInFuture($scope.tasksList, i + 1, selectedTag)) {
                  $scope.selectedTags.splice(index, 1);
                  index -= 1;
                  break
                }
              }

            }
          }

        }
      };


      /**
       * Check if a Tag is used in future plays.
       * @param tasks
       * @param nextIndex
       * @param tag
       * @returns {boolean}
       */
      var isTagUsedInFuture = function (tasks, nextIndex, tag) {

        if (nextIndex >= tasks.length)return false;

        for (var j = nextIndex; j < tasks.length; j++) {
          if (tasks[j].tags.indexOf(tag.name) > -1)return true
        }
        return false;
      };

      /**
       * Filter Previous Tasks during a restart from option
       */
      var filterPreviousTasks = function(){

        //var restore_point_task = projects.selectedProject.restorePoint && projects.selectedProject.restorePoint.replace("RPB", "EPB").split("-", 2).join("-");
        $scope.restore_point_task = projects.selectedProject && projects.selectedProject.restorePoint;
        if(!$scope.restore_point_task) return;

        $scope.restore_point_index = 0;

        for (var i = 0; i < $scope.selectedTags.length; i++) {
          if ($scope.selectedTags[i].name.toLowerCase().indexOf($scope.restore_point_task) > -1) {
            $scope.restore_point_index = i;
          }
        }

        if($scope.restore_point_index){
          $scope.selectedTags.splice(0, $scope.restore_point_index+1)
        }

      };

      /**
       * is Tag Selected
       * @param tag
       */
      $scope.isSelected = function (tag) {
        for (var i = 0; i < $scope.selectedTags.length; i++) {
          if (tag.name == $scope.selectedTags[i].name) {
            return true
          }
        }
        return false
      };

      /**
       * Subscribe to refresh when project selection changes
       */
      projects.subscribeCustom($scope, $scope.mergeAndGetTasksList);

      if (!$scope.dataLoaded && projects.selectedProject) {
        $scope.mergeAndGetTasksList();
      }

      $scope.$watch('additional_options.pre_validation', function (newValue, oldValue) {
        if (newValue) $scope.additional_options.post_validation = false;
        else $scope.selectedTags = [];
        filterTasks();
      });

      $scope.$watch('additional_options.post_validation', function (newValue, oldValue) {
        if (newValue) $scope.additional_options.pre_validation = false;
        else $scope.selectedTags = [];
        filterTasks();
      });

      resetAllLists();

    }
  }

  angular.module('ehcOzoneApp')
    .component('run', {
      templateUrl: 'app/ansible/run/run.html',
      controller: RunComponent
    });

})();
