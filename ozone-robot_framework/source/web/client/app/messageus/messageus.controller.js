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
  .controller('MessageusCtrl', ['$scope', '$http', '$mdDialog', 'message', 'title', 'theme', function ($scope,$http,$mdDialog, message, title, theme) {

    $scope.usermessage ='';
    $scope.message = message || "We are eager to hear from you.";
    $scope.title = title || "Email us";
    $scope.buttonIcon = 'send';
    $scope.theme = theme || "default";

    $scope.sendMessage = function(message){
      $scope.buttonIcon = 'refresh';
        $http.post('/api/users/email',{message:message}).then(
          function(response){

            $scope.buttonIcon = 'check';
            setTimeout(function(){
              $mdDialog.hide();
            },1000);

          },function(response){
            console.log(response.data);
            $scope.buttonIcon = 'error';
          })

    };

    $scope.close = function(){
      if($scope.success){
        $mdDialog.hide();
      }else{
        $mdDialog.hide();
      }

    };

  }]);
