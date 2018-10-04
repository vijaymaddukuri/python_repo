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
  .service('log', function ($sce, $timeout, ansi2html, $mdDialog) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    var LogService = this;

    LogService.getTrackingItems = function (logs) {

      var re = /(\{"?ozone_display_item.*})/g;
      var m = logs.match(re);
      if (m && m.length) {
        return m.map(function (item) {
          return JSON.parse(item)['ozone_display_item']
        });
      }

    };

    /**
     * Get Logs and calculate progress
     * @param tile
     * @param getLogsService
     * @returns {*}
     */
    LogService.getLogs = function (tile, getLogsService) {
      tile.loading = true;

      if (!tile) {
        return
      }

      getLogsService(tile.jobObject, function (successResponse) {
          tile.loading = false;
          //tile.logOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));

          if (typeof successResponse.data == 'object')
            successResponse.data = successResponse.data.join("\n")

          tile.logContent = successResponse.data;


          var trackingItems = LogService.getTrackingItems(successResponse.data);
          var re = /Stream :: close :: code: [1-9][0-9]*,/;
          var m = re.exec(successResponse.data);

          if (m !== null) {
            tile.progress = -1;
          } else {
            tile.progress = LogService.getProgress(trackingItems);
          }

          if (successResponse.data.indexOf("OZONE_PROGRAM_COMPLETED-failed") > -1 || tile.progress != -200 && tile.progress != 100 && tile.progress != -100 && (successResponse.data.indexOf("Stream :: close :: code: 0, signal: undefined") > -1 || successResponse.data.indexOf("OZONE_PROGRAM_COMPLETED") > -1)) {
            tile.progress = -1;
          }

          if (!tile.options) tile.options = {};

          if (tile.progress == 100) {
            tile.progressType = 'green';
            tile.label = '100%';
            tile.refreshLog = false;
            tile.state = 'SUCCESS';

            tile.logsAvailable = true;
            tile.stepsAvailable = true
          } else if (tile.progress == -200) {
            tile.progress = 100;
            tile.progressType = 'orange';
            tile.label = '!';
            tile.options.fgColor = 'orange';
            tile.state = 'WARNING';
            tile.refreshLog = false;

            tile.logsAvailable = true;
            tile.stepsAvailable = true;

          } else if (tile.progress < 0) {
            tile.progress = tile.progress * -1;
            tile.progressType = 'red';
            tile.label = '!';
            tile.options.fgColor = 'red';

            tile.state = 'FAIL';

            tile.refreshLog = false;

            tile.logsAvailable = true;
            tile.stepsAvailable = true;
            //tile.showLog = true;
          }
          else {
            tile.logsAvailable = true;
            tile.stepsAvailable = true;
            tile.progressType = 'blue';
            tile.label = tile.progress + '%';

            tile.state = 'RUNNING';

            tile.options.fgColor = '#8BC34A';
            tile.showSteps = true;
            if (!tile.refreshLog) {
              tile.refreshLog = true;
              LogService.getLogs(tile, getLogsService);
            }

          }
        },
        function (errorResponse) {
          tile.loading = false;
          tile.logOutput = errorResponse.data;
          tile.logContent = errorResponse.data;

        })
    };

    /**
     * Refresh Logs
     * @param tile
     * @param scope
     * @param getLogsService
     */
    LogService.refreshLogs = function (tile, scope, getLogsService) {
      if (tile.logRefreshTimer) {
        $timeout.cancel(tile.logRefreshTimer);
      }

      LogService.getLogs(tile, getLogsService);
      tile.logRefreshTimer = $timeout(
        function () {
          //$scope.getLogs(tile);
          if (tile.refreshLog) {
            LogService.refreshLogs(tile, scope, getLogsService);
          }
        },
        10000
      );

      if (scope) {
        scope.$on(
          "$destroy",
          function (event) {
            $timeout.cancel(tile.logRefreshTimer);
          }
        );
      }


    };

    /**
     * Get Progress
     * @param trackingItems
     * @returns {number}
     */
    LogService.getProgress = function (trackingItems) {
      var i = 0;
      var progress = 0;
      var error = false;
      var all_success_with_warnings = false;


      angular.forEach(trackingItems, function (item) {
        if (item.type === 'PROGRESS') {
          if (progress < parseInt(item.message))
            progress = parseInt(item.message)
        }
        if (item.type === 'ERROR') {
          error = true
        }
        if (item.type === 'ALLSUCCESSWARNING') {
          all_success_with_warnings = true
        }
      });

      if (all_success_with_warnings) return -200;
      if (error) return -1 * progress;
      return progress;

    };

    this.openMoreInfo = function (isDlgOpen, errMsg, title, theme) {
      if (isDlgOpen) return;
      isDlgOpen = true;

      //Pasing theme variable doesnt work
      var theme2 = theme;

      $mdDialog.show({
        template: '<md-dialog aria-label="Dialog" md-theme="{{theme}}">' +
        '<md-toolbar class="md-primary md-hue-2">' +
        '<div class="md-toolbar-tools">' +
        '<h2> {{title}} </h2>' +
        '<span flex></span>' +
        '<md-button class="md-icon-button" ng-click="closeDialog()">' +
        'x' +
        '</md-button>' +
        '</div>' +
        '</md-toolbar>' +
        '  <md-dialog-content layout-padding style="overflow-wrap: break-word;">' +
        '   <p class="logconsole" ng-if="!largeLogs" id="logContent" ng-bind-html="errMsg | replaceLineBreaks | colorizeLogs"></p>' +
        '   <div class="col-md-12" ng-if="largeLogs" >' +
        '     <div ui-ace="{showGutter: false, theme:\'twilight\',document:\'text\',mode:\'text\',firstLineNumber: 1000,onChange:codeChanged,onLoad:aceLoaded}" ng-model="errMsg" ng-readonly="true" style="height:800px;width:800px;"></div>' +
        '   </div>' +
        '  </md-dialog-content>' +
        '  <md-dialog-actions style="min-height: 70px;">' +
        '    <md-checkbox ng-model="additional_options.auto_scroll" style="margin-right:10px;">Auto Scroll</md-checkbox>' +
        '    <md-checkbox ng-model="additional_options.refresh_log" style="margin-right:30px;">Refresh Logs</md-checkbox>' +
        '    <md-input-container> <label> Lines: </label> <input type="number" ng-model="additional_options.lines" style="width:80px;"> </md-input-container>' +
        '    <div flex></div>' +
        '    <ng-md-icon icon="{{statusIcon}}" ng-class="{\'fa-spin\':statusIcon==\'refresh\'}" ng-if="statusIcon"></ng-md-icon>' +
        '    <md-button ng-click="closeDialog()" class="md-primary">' +
        '      Close Dialog' +
        '    </md-button>' +
        '  </md-dialog-actions>' +
        '</md-dialog>',
        locals: {
          errMsg: errMsg,
          theme2: theme2,
          title: title
        },
        controller: DialogController
      });
      function DialogController($scope, $interval, $mdDialog, $timeout, errMsg, theme2, title, logExplorer) {
        $scope.errMsg = errMsg;
        $scope.theme = theme2 || 'default';
        $scope.title = title || 'Message';
        $scope.statusIcon = '';
        $scope.largeLogs = false;
        $scope.additional_options = {auto_scroll: true, refresh_log: true, lines: 500};
        var logMap = {
          'Agent Logs': 'agent',
          'redis': 'redis',
          'kue': 'kue',
          'kueCmdProcessor': 'kueCmdProcessor',
          'kueTaskStatusProcessor': 'kueTaskStatusProcessor',
          'vRA Logs': 'vraLogs'
        };

        /**
         * Update Logs
         */
        var getLogs = function (type, lines) {
          if ($scope.additional_options.refresh_log) {
            $scope.statusIcon = 'refresh';
            logExplorer.getLogs(type, lines, function (response) {
              $scope.statusIcon = '';
              $scope.theme = 'default';
              // if(response.data && response.data.length > 300000){
              //   $scope.largeLogs = true;
              // }else{
              //   $scope.largeLogs = false;
              // }
              $scope.largeLogs = false;
              $scope.errMsg = response.data;
              scrollToBottom();
            }, function (response) {
              $scope.theme = 'red';
              $scope.errMsg = response.data;
              $scope.statusIcon = 'error';
            })
          }
        };

        /**
         * Cancel Log Refresh Timer
         */
        var cancelTimer = function () {
          if ($scope.stopTime) $interval.cancel($scope.stopTime);
        };

        /**
         * Close Dialogue
         */
        $scope.closeDialog = function () {
          cancelTimer();
          $mdDialog.hide();
          isDlgOpen = false;
        };

        var scrollToBottom = function () {
          if ($scope.additional_options.auto_scroll) {
            $timeout(function () {
              angular.element(document.getElementsByTagName("md-dialog-content")).scrollTop(angular.element(document.getElementsByTagName("md-dialog-content"))[0].scrollHeight)
            }, 100);
          }
        };


        // Fetch logs
        if (title in logMap) {
          $scope.stopTime = $interval(function () {
            getLogs(logMap[title], $scope.additional_options.lines);
          }, 5000);

          if ($scope) {
            $scope.$on("$destroy",
              function (event) {
                cancelTimer()
              }
            );
          }
          getLogs(logMap[title], $scope.additional_options.lines);
        }

      }

    };


  });
