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

class LoginController {
  constructor(Auth, $state, $scope, system) {
    //this.user = {password:'P@ssw0rd@1717'};
    this.errors = {};
    this.submitted = false;

    /*var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
     // Firefox 1.0+
     var isFirefox = typeof InstallTrigger !== 'undefined';
     // At least Safari 3+: "[object HTMLElementConstructor]"
     var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
     // Internet Explorer 6-11
     var isIE = /!*@cc_on!@*!/false || !!document.documentMode;
     // Edge 20+
     var isEdge = !isIE && !!window.StyleMedia;
     // Chrome 1+
     var isChrome = !!window.chrome && !!window.chrome.webstore;
     // Blink engine detection
     var isBlink = (isChrome || isOpera) && !!window.CSS;

     $scope.unsupported_browser = true;
     if(isChrome){
     $scope.unsupported_browser = false;
     }*/

    this.Auth = Auth;
    this.$state = $state;
    $scope.buttonIcon = '';
    $scope.buttontheme = '';

    this.login = function (form) {
      this.submitted = true;

      var user_email = this.user.email;

      // By default consider users with @ozone.com domain. This is the local domain name of users.
      if (user_email && user_email.indexOf("@") == -1 && user_email.indexOf("\\") == -1) {
        user_email += "@ozone.com"
      }

      if (form.$valid) {
        $scope.buttonIcon = 'refresh';
        this.Auth.login({
          email: user_email,
          password: this.user.password
        })
          .then(() => {
            // Logged in, redirect to home

            //this.$state.go('main');
            this.$state.go('projects');
            system.checkMasterPassword();
          })
          .catch(err => {
            this.errors.other = err.message;
            $scope.errmsg = err.message;
            $scope.buttonIcon = 'error';
            $scope.buttontheme = 'red';
          });
      }
    }

  }
}

angular.module('ehcOzoneApp')
  .controller('LoginController', LoginController);
