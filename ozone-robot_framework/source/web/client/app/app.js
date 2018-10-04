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

angular.module('ehcOzoneApp', [
  'ehcOzoneApp.auth',
  'ehcOzoneApp.admin',
  'ehcOzoneApp.constants',
  'ngCookies',
  'ngResource',
  'ngSanitize',
  'ui.router',
  'ui.bootstrap',
  'validation.match',
  'ngMaterial',
  'ngMdIcons',
  'ui.knob',
  'md.data.table',
  'angularMoment',
  'mdPickers',
  'ngMessages',
  'ngAnimate',
  'ngFileUpload',
  'angular-svg-round-progressbar',
  'toastr',
  'ngProgress',
  'btford.markdown',
  'ngJsonExportExcel',
  'ansiToHtml',
  'ui.ace',
  'sortable',
  'hljs',
  'aurbano.timespan',
  'angular-js-xlsx'
])
  .config(function($urlRouterProvider, $locationProvider) {
    $urlRouterProvider
      .otherwise('/projects');

    $locationProvider.html5Mode(true);
  })
  .config(function($mdThemingProvider) {
    $mdThemingProvider.definePalette('amazingPaletteName', {
      '50': '4e5052',
      '100': 'ffcdd2',
      '200': 'ef9a9a',
      '300': 'e57373',
      '400': 'ef5350',
      '500': '4e5052',
      '600': 'e53935',
      '700': 'd32f2f',
      '800': 'c62828',
      '900': 'b71c1c',
      'A100': 'ff8a80',
      'A200': 'ff5252',
      'A400': 'ff1744',
      'A700': 'd50000',
      'contrastDefaultColor': 'light',    // whether, by default, text (contrast)
                                          // on this palette should be dark or light
      'contrastDarkColors': ['50', '100', //hues which contrast should be 'dark' by default
        '200', '300', '400', 'A100'],
      'contrastLightColors': undefined    // could also specify this if default was 'dark'
    });

    var emcBlue = $mdThemingProvider.extendPalette('blue', {
      '500': '2c95dd'
    });

    $mdThemingProvider.definePalette('emcBlue', emcBlue);

    $mdThemingProvider.theme('default')
      .primaryPalette('emcBlue')
      // .accentPalette('cyan');

    $mdThemingProvider.theme('red')
      .primaryPalette('red');

    // $mdThemingProvider.theme('cyan')
    //   .primaryPalette('cyan');

    $mdThemingProvider.theme('orange')
      .primaryPalette('orange');

    $mdThemingProvider.theme('grey')
      .primaryPalette('grey');

    $mdThemingProvider.theme('green')
      .primaryPalette('green');

    $mdThemingProvider.theme('blue')
      .primaryPalette('blue');

    /*$mdThemingProvider.theme('white')
      .primaryPalette('white');*/

    $mdThemingProvider.theme('darkTheme')
      .dark();
  })
  .config(function($mdIconProvider){
    $mdIconProvider.icon('menu', './assets/images/menu.svg', 24);
  });
