'use strict';

angular.module('ehcOzoneApp')
  .service('time', function () {
    // AngularJS will instantiate a singleton by calling "new" on this function
    /**
     * Get Time Difference
     * @param timeDifference
     * @returns {{days: string, hours: number, minutes: number, seconds: number}}
     * @private
     */
    this.getTimeDifference = function (timeDifference) {

      var msec = timeDifference;
      if (msec < 0) msec = msec * -1;

      var hh = Math.floor(msec / 1000 / 60 / 60);
      msec -= hh * 1000 * 60 * 60;
      var mm = Math.floor(msec / 1000 / 60);
      msec -= mm * 1000 * 60;
      var ss = Math.floor(msec / 1000);
      msec -= ss * 1000;

      return {
        days: '0',
        hours: hh,
        minutes: mm,
        seconds: ss
      }
    };

  });
