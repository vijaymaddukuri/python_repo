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

class ConfigureSslCertsComponent {
  constructor($scope,projects,configure,$mdDialog,$timeout,$sce,ansi2html,log) {
    $scope.dataLoaded = false;

    $scope.configureCandidates = ['vipr']; //'vmware_vra','vmware_vro','vmware_vrb','vmware_vrops','vmware_vrapp','vmware_loginsight'

    $scope.selected = {};

    $scope.components = [];

    $scope.selectedProjectChanged = function(){
      $scope.dataLoaded = true;
      $scope.tiles = [];
      $scope.components = [];
      $scope.vcenter = {};
      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.vcenter){
        $scope.vcenter = projects.selectedProject.components.vcenter
      }

      if(projects.selectedProject && projects.selectedProject.components){
        angular.forEach($scope.configureCandidates,function(configureCandidate){
          angular.forEach(projects.selectedProject.components,function(value,key){
            if(configureCandidate === key) {
              value.objectType = key;

              var tempTile = angular.copy(value);
              tempTile.title = key.replace("_"," ").toUpperCase();
              tempTile.subtitle = value.name;
              tempTile.object = value;
              tempTile.objectType = key;

              $scope.components.push(tempTile);

              $scope.getconfigureInfo(tempTile);
            }
          })
        });

      }
    };

    $scope.getconfigureInfo = function(tile){
      tile.loading = true;
      configure.get(projects.selectedProject._id, tile.objectType, function(successResponse) {
          tile.loading = false;
          tile.configureObject = successResponse.data[successResponse.data.length - 1];

          if(tile.configureObject && tile.configureObject.logfile){
            var matches = tile.configureObject.logfile.match(/.*_(.*).log/);
            if(matches.length > 1)tile.logtime = matches[1];
          }

          tile.buttonText = 'Configure';

          if(tile.configureObject){
            $scope.refreshLogs(tile);
          }
        },
        function(errorResponse){
          tile.loading = false;
          tile.buttonText = 'Configure';
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
        });
    };

    $scope.generateCerts = function(event,component){

      var csrInfo = projects.selectedProject.components.ssl_cert_info;
      csrInfo.commonName = component.hostname;

      var configureData = {
        type: component.objectType,
        //type: component.objectType + '_ssl',
        refid: projects.selectedProject._id + "_" + component.objectType,
        project: projects.selectedProject,
        csrInfo: csrInfo
      };
      component.buttonicon = 'refresh';
      configure.generateCerts(configureData, function(successResponse){

        component.buttonicon = '';
        $scope.showDialog(event, successResponse.data, component)
      },function(errorResponse){
        console.log(errorResponse)
      });
    };

    $scope.progressType='blue';
    $scope.getLogs = function(tile){
      tile.loading = true;

      configure.getLogs(tile.configureObject,function(successResponse){
          tile.loading = false;
          tile.logOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));

          var trackingItems = log.getTrackingItems(successResponse.data);
          var re = /Stream :: close :: code: [1-9][0-9]*,/;
          var m = re.exec(successResponse.data);

          if(m !== null){
            tile.progress = -1;
          }else{
            tile.progress = $scope.getProgress(trackingItems);
          }

          if((successResponse.data.indexOf("Stream :: close :: code: 0, signal: undefined")>-1 || successResponse.data.indexOf("OZONE_PROGRAM_COMPLETED")>-1)){
            tile.progress = 100;
          }

          if(successResponse.data.indexOf("OZONE_PROGRAM_COMPLETED-failed")>-1){
            tile.progress = -1;
          }

          //$scope.showTrackingItems(tile,trackingItems);
          if(tile.progress == 100){
            tile.progressType='green';
            tile.label = '100%';
            tile.refreshLog = false;
            tile.buttonicon = 'done_all';
            tile.errmsg = 'Click to Reconfigure';
            tile.buttontheme = 'green';
            tile.buttonText = 'Configured';
            tile.logsAvailable = true;
            tile.stepsAvailable = true
          }else if(tile.progress == -200){
            tile.progress = 100;
            tile.progressType='orange';
            tile.label = '!';
            tile.buttonicon = 'done_all';
            tile.errmsg = 'Click to Retry';
            tile.buttontheme = 'orange';
            tile.refreshLog = false;
            tile.buttonText = 'Configured';
            tile.logsAvailable = true;
            tile.stepsAvailable = true;
            //tile.showLog = true;
          }else if(tile.progress < 0){
            tile.progress = tile.progress*-1;
            tile.progressType='red';
            tile.label = '!';
            tile.buttonicon = 'error';
            tile.errmsg = 'Click to Retry';
            tile.buttonText = 'Configure';
            tile.buttontheme = 'red';
            tile.refreshLog = false;
            tile.buttonText = 'Configure';
            tile.logsAvailable = true;
            tile.stepsAvailable = true;
            //tile.showLog = true;
          }
          else{
            tile.logsAvailable = true;
            tile.stepsAvailable = true;
            tile.buttontheme = 'default';
            tile.buttonicon = 'refresh';
            tile.progressType='blue';
            tile.label = tile.progress + '%';
            tile.buttonText = 'Configuring';
            tile.showSteps = true;
            if(!tile.refreshLog){
              tile.refreshLog = true;
              $scope.getLogs(tile);
            }

          }
        },
        function(errorResponse){
          tile.loading = false;
          tile.logOutput = "";
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
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

    $scope.refreshLogs = function(tile){
      if(tile.logRefreshTimer){
        $timeout.cancel( tile.logRefreshTimer );
      }

      $scope.getLogs(tile);
      tile.logRefreshTimer = $timeout(
        function(){
          //$scope.getLogs(tile);
          if(tile.refreshLog) {
            $scope.refreshLogs(tile);
          }
        },
        10000
      );

      $scope.$on(
        "$destroy",
        function( event ) {
          $timeout.cancel( tile.logRefreshTimer );
        }
      );

    };

    projects.subscribeCustom($scope,$scope.selectedProjectChanged);

    if(!$scope.dataLoaded){
      $scope.selectedProjectChanged()
    }

    var SCOPE = $scope;

    $scope.showDialog = function ($event, certData, component) {
      var parentEl = angular.element(document.body);
      $mdDialog.show({
        parent: parentEl,
        targetEvent: $event,
        template: '<md-dialog style="width:900px;">' +
        '  <md-dialog-content>' +
        '<div layout="row">' +
        '   <md-input-container>' +
        '     <label>CSR</label>' +
        '     <textarea ng-model="certData.csr" rows="25" md-select-on-focus style="width: 400px;font-size: 11px; font-family: monospace;line-height: 1;"></textarea>' +
        '   </md-input-container>' +
        '   <md-input-container>' +
        '     <label>Certificate</label>' +
        '     <textarea ng-model="certData.cert" rows="25" md-select-on-focus style="width: 400px;font-size: 11px; font-family: monospace;line-height: 1;" placeholder="Paste the certificate key here"></textarea>' +
        '   </md-input-container>' +
        '</div>' +
        '  </md-dialog-content>' +
        '  <md-dialog-actions>' +
        '    <md-button ng-click="closeDialog()" class="md-primary">' +
        '      Cancel' +
        '    </md-button>' +
        '    <md-button ng-click="showConfirm($event)" class="md-primary">' +
        '      Submit' +
        '    </md-button>' +
        '  </md-dialog-actions>' +
        '</md-dialog>',
        locals: {
          certData: certData,
          component: component
        },
        controller: DialogController
      });
      function DialogController($scope, $mdDialog, certData, component, configure) {
        $scope.certData = certData;
        $scope.closeDialog = function () {
          $mdDialog.hide();
        };

        $scope.showConfirm = function(event) {
          // Appending dialog to document.body to cover sidenav in docs app
          var confirm = $mdDialog.confirm()
            .title('Are you sure?')
            .textContent('System will reboot!')
            .ariaLabel('Confirm')
            .targetEvent(event)
            .ok('Yes')
            .cancel('No');
          $mdDialog.show(confirm).then(function() {
            $scope.processCertificate(event)
          }, function() {

          });
        };

        $scope.processCertificate = function(event){

          //component.private_key = certData.rsa_key;
          //component.certificate_chain = certData.cert;

          projects.selectedProject.components[component.objectType].private_key =certData.rsa_key;
          projects.selectedProject.components[component.objectType].certificate_chain =certData.cert;

          var configureData = {
            type: component.objectType + '_ssl',
            refid: projects.selectedProject._id + "_" + component.objectType + '_ssl',
            project: projects.selectedProject
          };
          component.buttonicon = 'refresh';


          configure.create(configureData, function(successResponse){
            component.refreshLog = true;
            component.configureObject = successResponse.data;
            component.buttontheme = 'green';
            var matches = component.configureObject.logfile.match(/.*_(.*).log/);
            if(matches.length > 1)component.logtime = matches[1];

            setTimeout(function(){
              SCOPE.refreshLogs(component);
            },6000);

            //
          },function(errorResponse){
            component.refreshLog = false;
            component.buttonicon = 'error';
            component.buttontheme = 'red';
            component.errmsg = errorResponse.data;
            console.log("errorResponse ="+ JSON.stringify(errorResponse.data));
            if(component.logRefreshTimer){
              $timeout.cancel( component.logRefreshTimer );
            }
            component.logOutput = errorResponse.data;
            component.logsAvailable = true;
            component.showLog = true;
          });
        };

      }
    }

  }
}

angular.module('ehcOzoneApp')
  .component('configureSslCerts', {
    templateUrl: 'app/configure/configure_ssl_certs/configure_ssl_certs.html',
    controller: ConfigureSslCertsComponent
  });

})();
