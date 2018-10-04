'use strict';

angular.module('ehcOzoneApp')
  .filter('colorizeLogs', function ($sce) {
    return function (input) {

      if(input && typeof input == 'object')input = JSON.stringify(input);

      if(input)
        return $sce.trustAsHtml(input.toString()
          .replace(/(.*?)\|(.*)/g,'<span style="color:mediumpurple;">$1</span> | $2')
          .replace(/\[INFO\]/g,'[<span style="color:deepskyblue;">INFO</span>]')
          .replace(/\[ERROR\]/g,'[<span style="color:red;">ERROR</span>]')
          .replace(/\[CRITICAL\]/g,'[<span style="color:red;">CRITICAL</span>]')
          .replace(/\[WARNING\]/g,'[<span style="color:orange;">WARNING</span>]')
        );
    };
  });
