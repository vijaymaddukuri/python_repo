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

class MonitorComponent {
  constructor($scope,$state,Auth,projects) {
    $scope.hasMonitorRole = Auth.hasRole('monitor');

    $scope.tabs = [{
      name: 'Status',
      route: 'monitor.status'
    },
    {
      name: 'Versions',
      route: 'monitor.versions'
    },
    {
      name: 'License',
      route: 'monitor.license'
    },
    {
      name: 'SSL Certificates',
      route: 'monitor.ssl_certs'
    }];


    angular.forEach($scope.tabs,function(tab){
      tab.isActive = tab.route == $state.current.name
    });

    $scope.go = function(route){
      $state.go(route)
    };

    projects.refresh();

  }
}

angular.module('ehcOzoneApp')
  .component('monitor', {
    templateUrl: 'app/monitor/monitor.html',
    controller: MonitorComponent
  });

})();
