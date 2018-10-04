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






// Karma configuration
// http://karma-runner.github.io/0.10/config/configuration-file.html

module.exports = function(config) {
  config.set({
    // base path, that will be used to resolve files and exclude
    basePath: '',

    // testing framework to use (jasmine/mocha/qunit/...)
    frameworks: ['jasmine'],

    // list of files / patterns to load in the browser
    files: [
      // bower:js
      'client/bower_components/jquery/jquery.js',
      'client/bower_components/angular/angular.js',
      'client/bower_components/angular-resource/angular-resource.js',
      'client/bower_components/angular-cookies/angular-cookies.js',
      'client/bower_components/angular-sanitize/angular-sanitize.js',
      'client/bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
      'client/bower_components/lodash/dist/lodash.compat.js',
      'client/bower_components/angular-ui-router/release/angular-ui-router.js',
      'client/bower_components/angular-validation-match/dist/angular-validation-match.min.js',
      'client/bower_components/angular-animate/angular-animate.js',
      'client/bower_components/angular-aria/angular-aria.js',
      'client/bower_components/angular-messages/angular-messages.js',
      'client/bower_components/angular-material/angular-material.js',
      'client/bower_components/angular-material-icons/angular-material-icons.min.js',
      'client/bower_components/jquery-knob/js/jquery.knob.js',
      'client/bower_components/angular-knob/src/angular-knob.js',
      'client/bower_components/angular-material-data-table/dist/md-data-table.js',
      'client/bower_components/moment/moment.js',
      'client/bower_components/angular-moment/angular-moment.js',
      'client/bower_components/mdPickers/dist/mdPickers.min.js',
      'client/bower_components/ng-file-upload/ng-file-upload.js',
      'client/bower_components/angular-svg-round-progressbar/build/roundProgress.js',
      'client/bower_components/svg-morpheus/compile/minified/svg-morpheus.js',
      'client/bower_components/wow/dist/wow.js',
      'client/bower_components/angular-toastr/dist/angular-toastr.tpls.js',
      'client/bower_components/ngprogress/build/ngprogress.min.js',
      'client/bower_components/showdown/src/showdown.js',
      'client/bower_components/angular-markdown-directive/markdown.js',
      'client/bower_components/oboe/dist/oboe-browser.js',
      'client/bower_components/angular-oboe/dist/angular-oboe.js',
      'client/bower_components/ng-csv/build/ng-csv.min.js',
      'client/bower_components/file-saver/FileSaver.js',
      'client/bower_components/json-export-excel/src/json-export-excel.js',
      'client/bower_components/angular-ui-ace/ui-ace.js',
      'client/bower_components/ace-builds/src-min-noconflict/ace.js',
      'client/bower_components/highlightjs/highlight.pack.js',
      'client/bower_components/blvd-sortable/dist/sortable.js',
      'client/bower_components/angular-highlightjs/build/angular-highlightjs.js',
      'client/bower_components/angular-timespan/dist/angular-timespan.min.js',
      'client/bower_components/angular-mocks/angular-mocks.js',
      // endbower
      'client/app/app.js',
      'client/{app,components}/**/*.module.js',
      'client/{app,components}/**/*.js',
      'client/{app,components}/**/*.html'
    ],

    preprocessors: {
      '**/*.html': 'ng-html2js',
      'client/{app,components}/**/*.js': 'babel'
    },

    ngHtml2JsPreprocessor: {
      stripPrefix: 'client/'
    },

    babelPreprocessor: {
      options: {
        sourceMap: 'inline'
      },
      filename: function (file) {
        return file.originalPath.replace(/\.js$/, '.es5.js');
      },
      sourceFileName: function (file) {
        return file.originalPath;
      }
    },

    // list of files / patterns to exclude
    exclude: [],

    // web server port
    port: 8080,

    // level of logging
    // possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
    logLevel: config.LOG_INFO,

    // reporter types:
    // - dots
    // - progress (default)
    // - spec (karma-spec-reporter)
    // - junit
    // - growl
    // - coverage
    reporters: ['spec'],

    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: false,

    // Start these browsers, currently available:
    // - Chrome
    // - ChromeCanary
    // - Firefox
    // - Opera
    // - Safari (only Mac)
    // - PhantomJS
    // - IE (only Windows)
    browsers: ['PhantomJS'],

    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: false
  });
};
