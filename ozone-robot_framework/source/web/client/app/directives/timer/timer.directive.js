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
  .directive('timer', function ($interval) {
    return {
      templateUrl: 'app/directives/timer/timer.html',
      restrict: 'EA',
      scope: {
        duration: '=?',
        days: '=?',
        hours: '=?',
        minutes: '=?',
        seconds: '=?',
        size: '=?',
        tick: '='
      },
      link: function (scope, element, attrs) {
        var stop;

        scope.size = scope.size || 'Large';

        if (scope.size == 'Large') {
          scope.timer_size = 40;
          scope.font_size = 50;
          scope.padding_top = 25;
          scope.margin_right = 20;
        } else {
          scope.timer_size = 20;
          scope.font_size = 20;
          scope.padding_top = 15;
          scope.margin_right = 0;
        }

        if (scope.duration && scope.duration.days) {
          scope.days = scope.duration.days
          scope.hours = scope.duration.hours
          scope.minutes = scope.duration.minutes
          scope.seconds = scope.duration.seconds
        }

        if (scope.tick) {
          stop = $interval(function () {

            if (!scope.tick && stop) {
              stopTicker()
            }

            scope.seconds += 1;
            if (scope.seconds > 59) {
              scope.seconds = 1;
              scope.minutes += 1;
              if (scope.minutes > 59) {
                scope.minutes = 0;
                scope.hours += 1;
                if (scope.hours > 23) {
                  scope.hours = 0
                  scope.days += 1
                }
              }
            }
          }, 1000)
        }


        var stopTicker = function () {

          if (angular.isDefined(stop)) {
            $interval.cancel(stop);
            stop = undefined;
          }
        };


        scope.$on('$destroy', function () {
          // Make sure that the interval is destroyed too
          stopTicker();
        });

      }
    };
  });
