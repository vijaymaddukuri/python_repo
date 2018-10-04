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

class StatusComponent {
  constructor($scope,projects,monitor,messageus,ansi2html,$sce ) {
    $scope.dataLoaded = false;
    $scope.monitorCandidates = ['vipr','vmware_vro'];

    $scope.showEmailUs = function(ev){
      messageus.showInputDialog(ev,"Count me In!","Tell us about yourself.","green");
    };

    $scope.selectedProjectChanged = function(){
      $scope.tiles = [];
      $scope.vcenter = {};
      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.vcenter){
        $scope.vcenter = projects.selectedProject.components.vcenter
      }

      if(projects.selectedProject && projects.selectedProject.components){
        angular.forEach($scope.monitorCandidates,function(configureCandidate){
          angular.forEach(projects.selectedProject.components,function(value,key){
            if(configureCandidate === key) {
              $scope[key] = value;
              var tempTile = angular.copy(baseTile);
              tempTile.title = key.replace("_"," ").toUpperCase();
              tempTile.subtitle = value.name;
              tempTile.object = value;
              tempTile.objectType = key;
              //tempTile.caption = '<b>IP:</b>' + $scope.vipr.network_vip + "<br>";

              $scope.tiles.push(tempTile);
              //var duplicateTile = angular.copy(tempTile);
              //$scope.tiles.push(duplicateTile);
              $scope.getMonitorInfo(tempTile);
            }
          })
        });

      }
    };

    var baseTile = {
      title: '',
      subtitle: '',
      caption: '',
      span:{row : 1, col : 6 },
      options : {
        width: 100,
        height: 100,
        fgColor: '#8BC34A',
        skin: 'tron',
        thickness: 0.1,
        displayPrevious: true,
        animationDelay: 200
      },
      type: 'knob',
      icon: 'computer',
      isTime: 'false',
      label: '',
      addStyle: '',
      object:{},
      objectType:'',
      refreshLog:false,
      showLog:false,
      configureObject:{},
      logOutput: '',
      progress: 0,
      buttonicon: 'refresh',
      errmsg: '',
      accessLink: '',
      loading: true,
      launchbuttontooltip:'Launch instance in a new window',
      accessLinkLive: false,
      trackingItems : [],
      buttonText : 'Checking',
      logsAvailable: false,
      stepsAvailable: false,
      logRefreshTimer:null,
      buttonspin:false
    };

    $scope.tiles = [];
    $scope.refreshLog = {value: false};
    $scope.result = null;

    $scope.progressType='blue';

    var customer_colors = {};
    customer_colors['green'] = '#2e7d32';
    customer_colors['red'] = '#c62828';
    customer_colors['blue'] = '#1565c0';
    customer_colors['grey'] = 'grey';

    $scope.getMonitorInfo = function(tile){
      tile.loading = true;
      tile.trackingItems = [];

      var monitorData = {
        type: tile.objectType,
        refid: projects.selectedProject._id + "_" + tile.objectType,
        project: projects.selectedProject
      };
      tile.buttonicon = 'refresh';
      tile.buttonspin = true;
      tile.progress = 0;
      monitor.getStatus(monitorData,
        function(successResponse){
          tile.buttonspin = false;

          tile.loading = false;
          tile.logOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));

          var trackingItem = $scope.getTrackingItems(successResponse.data)[0];

          if(trackingItem){
            tile.progressType=trackingItem['color'];
            tile.options.fgColor=customer_colors[trackingItem['color']];
            tile.label = trackingItem['cluster_state'] || trackingItem['overall_state'];
            tile.progress = 100;
            tile.buttonicon = 'refresh';
            $scope.showTrackingItems(tile,trackingItem['detail']);
          }

        },
        function(errorResponse){
          tile.loading = false;
          tile.buttonspin = false;
          tile.label = 'N/A';
          tile.options.fgColor = 'grey';
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
          tile.logOutput = JSON.stringify(errorResponse.data)
        })
    };

    $scope.getProgress = function(trackingItems){
      var i = 0;
      var progress = 0;
      var error = false;
      var all_success_with_warnings = false;


      angular.forEach(trackingItems,function(item){
        if(item.type==='PROGRESS'){
          if(progress < parseInt(item.message) )
            progress = parseInt(item.message)
        }
        if(item.type==='ERROR') {
          error = true
        }
        if(item.type==='ALLSUCCESSWARNING') {
          all_success_with_warnings = true
        }
      });

      if(all_success_with_warnings) return -200;
      if(error) return -1 * progress;
      return progress;

    };

    $scope.showTrackingItems = function(tile,trackingItems){
      var i = 0;
      var unique_dict = {};
      tile.trackingItems = [];
      angular.forEach(trackingItems,function(item){

          if(item.state === 'ALLSUCCESS') {
            item.icon = 'done_all';
            item.color = '#2e7d32'
          }else if(item.state === 'ALLSUCCESSWARNING') {
            item.icon = 'done_all';
            item.color = 'orange'
          }else if(item.state === 'Good'){
            item.icon = 'check_circle';
            item.color = '#2e7d32'
          }else if(item.state === 'ERROR'){
            item.icon = 'error';
            item.color = '#c62828'
          }else if(item.state === 'RUNNING'){
            item.icon = 'refresh';
            item.color = '#1565c0'
          }else if(item.state === 'PENDING'){
            item.icon = 'alarm';
            item.color = '#1565c0'
          }else{
            item.icon = 'error';
            item.color = 'orange'
          }

          var trackItemExists = false;
          angular.forEach(tile.trackingItems,function(trackItem){
            if(trackItem.item == item.item){
              trackItemExists = true;
              trackItem.state = item.state;
              trackItem.icon = item.icon;
              trackItem.color = item.color;
            }
          });

          if(!trackItemExists){
            tile.trackingItems.push(item)
          }

      });

      //tile.trackingItems = unique_dict

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

    $scope.getStyle = function(isSemi,radius, time, color){
      var transform = (isSemi ? '' : 'translateY(-50%) ') + 'translateX(-50%)';
      if(time){
        return {
          'top': isSemi ? 'auto' : '60%',
          'bottom': isSemi ? '5%' : 'auto',
          'left': '50%',
          'transform': transform,
          '-moz-transform': transform,
          '-webkit-transform': transform,
          'font-size': '15px',
          'color': color,
          'font-weight': 'lighter'
        };
      }else {

        return {
          'top': isSemi ? 'auto' : '60%',
          'bottom': isSemi ? '5%' : 'auto',
          'left': '50%',
          'transform': transform,
          '-moz-transform': transform,
          '-webkit-transform': transform,
          'font-size': '15px',
          'font-weight': 'lighter',
          'color':color
        };
      }
    };

  }
}

angular.module('ehcOzoneApp')
  .component('status', {
    templateUrl: 'app/monitor/status/status.html',
    controller: StatusComponent
  });

})();
