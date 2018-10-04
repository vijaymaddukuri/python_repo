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

class LicenseComponent {
  constructor($scope,projects,monitor,ansi2html,$sce) {

    $scope.monitorCandidates = ['vipr','vmware_vro','vcenter'];

    $scope.selected = {};
    $scope.dataLoaded = false;

    $scope.components = [];

    $scope.selectedProjectChanged = function(){
      $scope.dataLoaded = true;
      $scope.tiles = [];
      $scope.vcenter = {};
      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.vcenter){
        $scope.vcenter = projects.selectedProject.components.vcenter
      }

      if(projects.selectedProject && projects.selectedProject.components){
        angular.forEach($scope.monitorCandidates,function(configureCandidate){
          angular.forEach(projects.selectedProject.components,function(value,key){
            if(configureCandidate === key) {

              var component = {
                name: key.replace("_"," ").toUpperCase(),
                objectType: key
              };
              $scope.components.push(component);

              $scope.getLicenseInfo(component);
            }
          })
        });

      }
    };

    $scope.progressType='blue';

    var customer_colors = {};
    customer_colors['green'] = '#2e7d32';
    customer_colors['red'] = '#c62828';
    customer_colors['blue'] = '#1565c0';
    customer_colors['grey'] = 'grey';

    $scope.getLicenseInfo = function(component){
      component.loading = true;
      component.trackingItems = [];

      var baseComponent = angular.copy(component);

      var monitorData = {
        type: component.objectType,
        refid: projects.selectedProject._id + "_" + component.objectType,
        project: projects.selectedProject
      };

      monitor.getLicense(monitorData,
        function(successResponse){

          component.logOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));
          component.loading = false;
          angular.forEach($scope.getTrackingItems(successResponse.data),function(trackingItem, index){

            if(index > 0){
              component = angular.copy(baseComponent)
            }

            if(trackingItem && 'license' in trackingItem){
              component.license = trackingItem.license;
            }

            if(index > 0) {
              $scope.components.push(component)
            }
            component.loading = false;
          });


        },
        function(errorResponse){
          component.loading = false;
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data));
          component.logOutput = JSON.stringify(errorResponse.data)
        })
    };


    $scope.getTrackingItems = function(logs){
      //Sample result
      //{"ozone_result_item": {"color": "green", "detail": [{"item": "10.247.69.62", "details": [{"name": "dbsvc", "status": "Good"}, {"name": "authsvc", "status": "Good"}, {"name": "sasvc", "status": "Good"}, {"name": "apisvc", "status": "Good"}, {"name": "controllersvc", "status": "Good"}, {"name": "geodbsvc", "status": "Good"}, {"name": "geosvc", "status": "Good"}, {"name": "coordinatorsvc", "status": "Good"}, {"name": "vasasvc", "status": "Good"}, {"name": "portalsvc", "status": "Good"}, {"name": "syssvc", "status": "Good"}], "state": "Good"}], "overall_state": "GOOD", "cluster_state": "STABLE"}}
      var filtered_results = logs.split("\n").filter(function(item){return item.indexOf('ozone_result_item') > -1});
      return filtered_results.map(function(item){
        try{
          return JSON.parse(item)['ozone_result_item'];
        }
        catch(e){
          console.log("Error - " + e);
          return {'type':'WARNING','message':'Error parsing step from log'}
        }
      });

    };

    projects.subscribeCustom($scope,$scope.selectedProjectChanged);

    if(!$scope.dataLoaded){
      $scope.selectedProjectChanged()
    }

  }
}

angular.module('ehcOzoneApp')
  .component('license', {
    templateUrl: 'app/monitor/license/license.html',
    controller: LicenseComponent
  });

})();
