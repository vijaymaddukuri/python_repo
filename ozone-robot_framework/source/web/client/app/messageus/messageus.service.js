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
  .service('messageus', function ($mdDialog, $mdMedia, $http) {
    // AngularJS will instantiate a singleton by calling "new" on this function
    this.showInputDialog = function (ev, title, message, theme) {
      //var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
      $mdDialog.show({
        controller: 'MessageusCtrl',
        //templateUrl: '/app/messageus/messageus.html',
        template: '<md-dialog aria-label="Message Us" md-theme="{{theme}}">' +
                      '     <form>' +
                      '       <md-toolbar class="md-primary md-hue-2">' +
                      '        <div class="md-toolbar-tools">' +
                      '        <h2>{{title}}</h2>' +
                      '      <span flex></span>' +
                      '      <md-button class="md-icon-button" ng-click="cancel()">' +
                      '' +
                      '        </md-button>' +
                      '        </div>' +
                      '        </md-toolbar>' +
                      '        <md-dialog-content>' +
                      '        <div class="md-dialog-content">' +
                      '        <!--<md-input-container>' +
                      '        <label>{{message}}</label>' +
                      '      </md-input-container>-->' +
                      '      <h3>{{message}}</h3>' +
                      '      <md-input-container>' +
                      '      <label>Message</label>' +
                      '      <textarea ng-model="usermessage" md-maxlength="150" rows="5" md-select-on-focus style="width:500px;"></textarea>' +
                      '' +
                      '        </md-input-container>' +
                      '        <div>' +
                      '        <md-button ng-click="sendMessage(usermessage)">' +
                      '        Send' +
                      '        <md-icon ng-md-icon icon="{{buttonIcon}}" ng-class="{\'fa-spin\' : buttonIcon == \'refresh\'}"></md-icon>' +
                      '        </md-button>' +
                      '        <md-button ng-click="close()" ><!--ng-show="success || error"-->' +
                      '        Close' +
                      '        </md-button>' +
                      '        </div>' +
                      '        </div>' +
                      '        </md-dialog-content>' +
                      '        <!--<md-dialog-actions layout="row">' +
                      '        <span flex></span>' +
                      '      <md-button ng-click="answer("cancel"")">' +
                      '        Cancel' +
                      '        </md-button>' +
                      '        <md-button ng-click="answer("create")">' +
                      '        Create' +
                      '        </md-button>' +
                      '        </md-dialog-actions>-->' +
                      '        </form>' +
                      '        </md-dialog>',

        parent: angular.element(document.body),
        targetEvent: ev,
        locals: {
          message: message,
          title: title,
          theme: theme
        }
        /*clickOutsideToClose:true,*/
        //fullscreen: useFullScreen
      })
        .then(function (answer) {

        }, function () {

        });
      /*$scope.$watch(function() {
       return $mdMedia('xs') || $mdMedia('sm');
       }, function(wantsFullScreen) {
       //$scope.customFullscreen = (wantsFullScreen === true);
       });*/
    };

    this.emailUs = function (subject, message) {
      $http.post('/api/users/email', {message: message, subject: subject}).then(
        function (response) {

        }, function (response) {
          console.log(response.data);
        })
    }

  });
