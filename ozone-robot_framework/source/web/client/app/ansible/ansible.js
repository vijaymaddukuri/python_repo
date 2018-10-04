'use strict';

angular.module('ehcOzoneApp')
  .config(function ($stateProvider) {
    $stateProvider
      .state('deploy', {
        url: '/deploy',
        template: '<ansible></ansible>',
        authenticate: 'user'
      });
  });
