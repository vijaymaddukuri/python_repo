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

class DashboardComponent {
  constructor($scope,projects,$rootScope,dashboard) {
    $scope.dashboardCandidates = ['vcenter','vipr','viprsrm','vmware_vra','vmware_vro','vmware_vrb','vmware_vrops','vmware_vrapp'];

    $scope.dataLoaded = false;

    /*projects.getProjects(function(response){
      $scope.projects = response.data;
      projects.selectedProject = $scope.projects[0];

      //$scope.progressbar.complete();
    });

    $scope.$watch('selectedProject',function(newValue,oldValue){
      $scope.processSelectedProject();
    });
*/
    $scope.selectedProjectChanged = function(){
      $scope.dataLoaded = true;
      $scope.tiles = dashboard.getDashboardTiles();
      $scope.vcenter = {};
      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.vcenter){
        $scope.vcenter = projects.selectedProject.components.vcenter
      }

      if(projects.selectedProject && projects.selectedProject.components){
        var i=1;
        angular.forEach(projects.selectedProject.components,function(value,key){

          $scope[key] = value;
          var tempTile = $scope.getTileByType(key);
          if(tempTile){
            tempTile.disabledStyle="";
            tempTile.title = key.replace("_"," ").toUpperCase();
            tempTile.subtitle = value.name;
            tempTile.object = value;
            tempTile.enabled = true;
            tempTile.objectType = key;
            tempTile.accessLinkLive = true;
            tempTile.label='';
            tempTile.launchbuttonicon = 'launch';
            //setTimeout($scope.getAccessLinkStatus(tempTile),i * 1000);
            i++;
          }else{
            console.error("cannot find key " + key);
          }

        })
      }
    };

    $scope.getAccessLinkStatus = function(tile){
      return function (){
        $scope.getAccessLink(tile,false);
      }
    };

    $scope.getAccessLink = function(tile,returnContent){
      tile.launchbuttonicon = 'refresh';
      tile.launchbuttontooltip = 'Checking Status';
      tile.accessLinkLive = false;

      /*deploy.getLinkStatus(tile.object.accessLink,returnContent,
        function(successResponse){
          //


          tile.accessLinkLive = true;
          tile.launchbuttonicon = 'launch';
          tile.count = 100;
          tile.label='OK';
          tile.launchbuttontooltip = 'Application Ready. Click to Launch.';
        },
        function(errorResponse){
          console.log("Error response on get status link");
          console.log(errorResponse.data);
          tile.accessLinkLive = false;
          tile.launchbuttonicon = 'error';
          tile.launchbuttontooltip = errorResponse.data;
          tile.label='!';
          //console.error(errorResponse.data);
        })*/
    };

    $scope.getTileByType = function(type){
      var result=null;
      angular.forEach($scope.tiles,function(tile,index){
        if(tile.objtype === type){
          result = tile;
        }
      });

      return result;
    };

    projects.subscribeCustom($scope,$scope.selectedProjectChanged);

    if(!$scope.dataLoaded){
      $scope.selectedProjectChanged()
    }

    $rootScope.$emit('notify-refresh-projects');

    $scope.getStyle = function(isSemi,radius, time, color){
      var transform = (isSemi ? '' : 'translateY(-50%) ') + 'translateX(-50%)';
      if(time){
        return {
          'top': isSemi ? 'auto' : '23px',
          '-moz-top': isSemi ? 'auto' : '35%',
          'bottom': isSemi ? '5%' : 'auto',
          'left': '50%',
          'transform': transform,
          '-moz-transform': transform,
          '-webkit-transform': transform,
          'font-size': radius / 3.4 + 'px',
          'color': color,
          'font-weight': 'bold'
        };
      }else {

        return {
          'top': isSemi ? 'auto' : '23px',
          '-moz-top': isSemi ? 'auto' : '35%',
          'bottom': isSemi ? '5%' : 'auto',
          'left': '50%',
          'transform': transform,
          '-moz-transform': transform,
          '-webkit-transform': transform,
          'font-size': radius / 3.4 + 'px',
          'color':color
        };
      }
    };
  }
}

angular.module('ehcOzoneApp')
  .component('dashboard', {
    templateUrl: 'app/dashboard/dashboard.html',
    controller: DashboardComponent
  });

})();
