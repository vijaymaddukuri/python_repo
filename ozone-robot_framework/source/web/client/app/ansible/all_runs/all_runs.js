'use strict';

angular.module('ehcOzoneApp')
  .config(function ($stateProvider) {
    $stateProvider
      .state('all_runs', {
        url: '/ansible/all_runs',
        template: '<all-runs></all-runs>'
      });
  });
