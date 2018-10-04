'use strict';

angular.module('ehcOzoneApp')
  .config(function ($stateProvider) {
    $stateProvider
      .state('system', {
        url: '/system',
        template: '<system></system>',
        authenticate: 'user'
      });
  });
