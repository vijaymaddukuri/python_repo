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
  .service('tile', function () {
    // AngularJS will instantiate a singleton by calling "new" on this function
    this.getBaseTile = function(){
      return {
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
          animationDelay: 700
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
        buttonicon: '',
        errmsg: '',
        accessLink: '',
        loading: true,
        launchbuttontooltip:'Launch instance in a new window',
        accessLinkLive: false,
        trackingItems : [],
        buttonText : 'Checking',
        logsAvailable: false,
        stepsAvailable: false,
        logRefreshTimer:null
      };
    };

    /**
     * Get Component tiles to display in page
     * @param selectedProject
     * @param candidates
     * @param tiles
     * @param getDataCall
     */
    this.getComponentTiles = function(selectedProject,candidates,tiles,getDataCall){
      var tileService = this;
      if(selectedProject && selectedProject.components && selectedProject.components.import_data && selectedProject.components.import_data.hosts){
        angular.forEach(candidates,function(candidate){
          angular.forEach(selectedProject.components.import_data.hosts,function(host){
            if(candidate === host.name) {
              //$scope[key] = value;
              var tempTile = angular.copy(tileService.getBaseTile());
              tempTile.title = host.name.replace("_"," ").toUpperCase();
              tempTile.subtitle = host.ip;
              tempTile.ip = host.ip;
              //tempTile.object = value;
              tempTile.objectType = host.name;
              tiles.push(tempTile);
              getDataCall(tempTile);
            }
          })
        });

      }
    };

    this.getStyle = function(isSemi,radius, time, color){
      var transform = (isSemi ? '' : 'translateY(-50%) ') + 'translateX(-50%)';
      if(time){
        return {
          'top': isSemi ? 'auto' : '40%',
          'bottom': isSemi ? '5%' : 'auto',
          'left': '50%',
          'transform': transform,
          '-moz-transform': transform,
          '-webkit-transform': transform,
          'font-size': radius / 2.5 + 'px',
          'color': color,
          'font-weight': 'bold'
        };
      }else {

        return {
          'top': isSemi ? 'auto' : '45%',
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

  });
