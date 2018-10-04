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
  .controller('MenuCtrl', function () {
    //.controller('MenuCtrl', function ($scope, $timeout, $mdSidenav, $log) {
    /*$scope.message = 'Hello';

    //$scope.toggleLeft = buildDelayedToggler('left');
    //$scope.toggleRight = buildToggler('right');
    // $scope.isOpenRight = function(){
    //   return $mdSidenav('right').isOpen();
    // };

    /!**
     * Supplies a function that will continue to operate until the
     * time is up.
     *!/
    function debounce(func, wait, context) {
      var timer;
      return function debounced() {
        var context = $scope,
          args = Array.prototype.slice.call(arguments);
        $timeout.cancel(timer);
        timer = $timeout(function() {
          timer = undefined;
          func.apply(context, args);
        }, wait || 10);
      };
    }
    /!**
     * Build handler to open/close a SideNav; when animation finishes
     * report completion in console
     *!/
    function buildDelayedToggler(navID) {

      return debounce(function() {

        $mdSidenav(navID)
          .toggle()
          .then(function () {
            $log.debug('toggle ' + navID + ' is done');

          });
      }, 200);
    }
    function buildToggler(navID) {

      return function() {

        $mdSidenav(navID)
          .toggle()
          .then(function () {
            $log.debug('toggle ' + navID + ' is done');
          });
      }
    }*/

  });
