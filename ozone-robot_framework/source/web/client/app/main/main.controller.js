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

(function() {

class MainController {

  constructor($scope,$rootScope,$mdDialog,$http) {
    $rootScope.hideMenu = true;

    $scope.$on("$destroy",function(){
      $rootScope.hideMenu = false;
    });

    $scope.showVideo = function(ev){
      var  video_url = 'assets/videos/Ozone.mp4';
      $mdDialog.show({
        //controller: DialogController,
        template:'<div style="height:455px; width:795px;"  class="embed-responsive embed-responsive-16by9">' +
        '<video autoplay controls height="450" width="795" class="embed-responsive-item" src="' + video_url + '"></video>' +
        '</div>',
        targetEvent: ev,
        clickOutsideToClose: true
      });
    };

    $scope.buttonIcon = 'send';

    $scope.sendMessage = function(message){
      $scope.buttonIcon = 'refresh';
      $http.post('/api/users/email',{message:message}).then(
        function(response){

          $scope.buttonIcon = 'check';
          $scope.usermessage = '';
        },function(response){
          console.log(response.data);
          $scope.buttonIcon = 'error';
        })

    };

  }

}

angular.module('ehcOzoneApp')
  .component('main', {
    templateUrl: 'app/main/main.html',
    controller: MainController
  });

})();
