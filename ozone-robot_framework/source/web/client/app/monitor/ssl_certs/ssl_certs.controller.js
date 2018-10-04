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

class SslCertsComponent {
  constructor($scope,projects,$sce,monitor,ansi2html) {
    $scope.dataLoaded = false;

    $scope.monitorCandidates = ['vipr','vcenter','viprsrm','vmware_vra','vmware_vro','vmware_vrb','vmware_vrops','vmware_vrapp','vmware_loginsight']; //'vipr','vcenter',

    $scope.certIcons = {
      'CN':'',
      'C':'',
      'ST':'',
      'L':'',
      'O':'',
      'OU':''
    };

    $scope.selected = {};

    $scope.components = [];

    //Regex to get hostname from URL
    //var hostnameregex = /https?\:\/\/([^\/:?#]+)(?:[\/:?#]|$)/i; //regex for only hostname
    var hostnameregex = /https?\:\/\/([^\/?#]+)(?:[\/:?#]|$)/i;  //regex for hostname with port

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

              if(value.accessLink.indexOf('https') > -1){
                var hostname_match = hostnameregex.exec(value.accessLink);

                var component = {
                  name: key.replace("_"," ").toUpperCase(),
                  objectType: key
                };
                $scope.components.push(component);

                if(hostname_match && hostname_match.length){
                  var hostname = hostname_match[1];
                  if(hostname.indexOf(":") < 0)hostname += ':443';
                  component.accessLink = hostname;
                  $scope.getCertificateInfo(component);
                }else{
                  component.accessLink = "Couldn't identify a URL to check"
                }
              }

            }
          })
        });

      }
    };



    var customer_colors = {};
    customer_colors['green'] = '#2e7d32';
    customer_colors['red'] = '#c62828';
    customer_colors['blue'] = '#1565c0';
    customer_colors['grey'] = 'grey';

    $scope.getCertificateInfo = function(component){
      component.loading = true;
      component.trackingItems = [];

      var baseComponent = angular.copy(component);

      var monitorData = {
        type: 'ssl_certs',
        URL: component.accessLink,
        refid: projects.selectedProject._id + "_" + component.objectType,
        project: projects.selectedProject
      };

      monitor.getSSLCertificate(monitorData,
        function(successResponse){

          component.logOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));
          component.loading = false;
          $scope.checkForCertInfo(successResponse.data, component);
          /*angular.forEach($scope.getTrackingItems(successResponse.data),function(trackingItem, index){

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
          });*/


        },
        function(errorResponse){
          component.loading = false;
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data));
          $scope.checkForCertInfo(errorResponse.data, component);

        })
    };

    $scope.checkForCertInfo = function(data,component){
      component.logOutput = JSON.stringify(data);

      var result_matching_regex = /issuer=(.*?)\nsubject=(.*?)\n/g;
      var results = result_matching_regex.exec(data);

      if(results){
        component.certificate = {};
        component.issuer = {};
        $scope.getCertificateItemsArray(results[1].trim(),component.certificate);
        $scope.getCertificateItemsArray(results[2].trim(),component.issuer);

      }

      //Get dates
      result_matching_regex = /notBefore=(.*?)\nnotAfter=(.*?)\n/g;
      results = result_matching_regex.exec(data);

      if(results){
        component.certificate.startDate = results[1];
        component.certificate.endDate = results[2]

      }

    };

    //certString = /CN=VMware/O=VMware, Inc./OU=vCAC Self Signed Certificate/C=US
    $scope.getCertificateItemsArray = function(certString,component){
        var re = /(.*?)=(.*?)(\/|$)/g;
        var matches = certString.match(re);
        var results = [];
        if(matches.length){
          results = matches.map(function(match){                //CN=VMware
                var match_type = match.split("=")[0].replace("/","");   //CN
                var match_value = (match.split("=")[1]).replace("/","");  //VMware
                component[match_type] = match_value;
                return {type:match_type, value:match_value}

            });
          return results
        }

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
  .component('sslCerts', {
    templateUrl: 'app/monitor/ssl_certs/ssl_certs.html',
    controller: SslCertsComponent
  });

})();
