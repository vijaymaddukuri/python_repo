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

class VersionsComponent {
  constructor($scope,projects,monitor,messageus,ansi2html,$sce,popup) {

    $scope.monitorCandidates = ['vipr','vmware_vro','vcenter','vmware_vrops','vmware_vra','vmware_vrapp','vmware_vrb','vmware_loginsight'];

    $scope.selected = {};
    $scope.dataLoaded = false;

    $scope.showEmailUs = function(ev){
      messageus.showInputDialog(ev,"Count me In!","Tell us about yourself.","green");
    };

    $scope.components = [];

    $scope.selectedProjectChanged = function(){
      $scope.dataLoaded = true;
      $scope.tiles = [];
      $scope.vcenter = {};
      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.vcenter){
        $scope.vcenter = projects.selectedProject.components.vcenter;
        $scope.supported_versions = projects.selectedProject.components.supported_versions;
      }

      if(!projects.selectedProject.components.supported_versions){
        popup.showAlert(null,"Supported Versions","Please update supported versions at Design -> General -> Supported Versions")
        return
      }

      if(projects.selectedProject && projects.selectedProject.components){
        angular.forEach($scope.monitorCandidates,function(configureCandidate){
          angular.forEach(projects.selectedProject.components,function(value,key){
            if(configureCandidate === key) {

              var component = {
                name: key.replace("_"," ").toUpperCase(),
                objectType: key,
                supported_version: $scope.supported_versions[key]
              };

              $scope.components.push(component);
              $scope.getVersionInfo(component);
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


    $scope.getVersionInfo = function(tile){
      tile.loading = true;
      tile.trackingItems = [];

      var monitorData = {
        type: tile.objectType,
        refid: projects.selectedProject._id + "_" + tile.objectType,
        project: projects.selectedProject
      };

      monitor.getVersion(monitorData,
        function(successResponse){
          tile.buttonspin = false;

          tile.loading = false;
          tile.logOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));

          var trackingItem = $scope.getTrackingItems(successResponse.data)[0];
          if(trackingItem && 'version' in trackingItem){
            tile.version = trackingItem.version.version;
          }
        },
        function(errorResponse){
          tile.loading = false;
          tile.buttonspin = false;
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data));
          tile.logOutput = JSON.stringify(errorResponse.data)
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
  .component('versions', {
    templateUrl: 'app/monitor/versions/versions.html',
    controller: VersionsComponent
  });

})();
