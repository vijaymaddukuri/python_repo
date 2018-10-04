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

class NavbarController {
  //start-non-standard
  menu = [{
    'title': 'Home',
    'state': 'main'
  }];

  isCollapsed = true;
  //end-non-standard


  constructor(Auth, $scope, messageus, $rootScope, projects, system, $interval) {
    $scope.selectedProject = null;

    this.isLoggedIn = Auth.isLoggedIn;
    this.isAdmin = Auth.isAdmin;
    this.getCurrentUser = Auth.getCurrentUser;

    $scope.showEmailUs = function(ev){
      messageus.showInputDialog(ev);
    };

    /**
     * On Project Change
     * @param project
     */
    $scope.projectChanged = function(project){
      projects.selectedProject = project;
      localStorage.selectedProjectID = null;
      if(project && project._id){
        localStorage.selectedProjectID = project._id;
        projects.notify();
      }

    };


    /**
     * Get all Projects
     */
    $rootScope.getProjects = function(){
      projects.getProjects(function(response){
        $scope.projects = response.data;
        if($scope.projects.length == 0){
          $scope.selectedProject = null;
        }else{
          $scope.selectedProject = $scope.getProjectById(localStorage.selectedProjectID) || $scope.projects[0];
        }
        $scope.projectChanged($scope.selectedProject);
        //$rootScope.$broadcast('projectLoaded');
      },function(response){
        console.log(response)
      });
    };

    /**
     * Get Project by ID
     * @param id
     * @returns {*}
     */
    $scope.getProjectById = function(id){
      var result;
      angular.forEach($scope.projects, function(project){
        if(project._id == id){
          result = project
        }
      });
      return result
    };

    //$scope.getProjects();

    $rootScope.$on('notify-refresh-projects', function(){
      $rootScope.getProjects();
    });

    var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
    // Firefox 1.0+
    var isFirefox = typeof InstallTrigger !== 'undefined';
    // At least Safari 3+: "[object HTMLElementConstructor]"
    var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
    // Internet Explorer 6-11
    var isIE = /*@cc_on!@*/false || !!document.documentMode;
    // Edge 20+
    var isEdge = !isIE && !!window.StyleMedia;
    // Chrome 1+
    var isChrome = !!window.chrome && !!window.chrome.webstore;
    // Blink engine detection
    var isBlink = (isChrome || isOpera) && !!window.CSS;

    $rootScope.unsupported_browser = true;
    if(isChrome || isFirefox){
      $rootScope.unsupported_browser = false;
    }

    $rootScope.$on('$stateChangeStart',
      function(event, toState, toParams, fromState, fromParams, options){

      });

    /**
     * Check if Master Password is set
     */
    $rootScope.isMasterPasswordSet = true;
    system.checkMasterPassword();

    var masterPolling = $interval(function(){
      system.checkMasterPassword();
    }, 60000);

    // Stop Master polling on scope destroy
    $scope.$on('$destroy', function () {
      masterPolling();
    });

    $scope.showSetMasterPasswordDialog = function(){
      system.showSetMasterPasswordDialog();
    }

  }
}

angular.module('ehcOzoneApp')
  .controller('NavbarController', NavbarController);
