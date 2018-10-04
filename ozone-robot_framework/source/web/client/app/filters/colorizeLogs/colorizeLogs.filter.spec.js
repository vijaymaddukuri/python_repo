'use strict';

describe('Filter: colorizeLogs', function () {

  // load the filter's module
  beforeEach(module('ehcOzoneApp'));

  // initialize a new instance of the filter before each test
  var colorizeLogs;
  beforeEach(inject(function ($filter) {
    colorizeLogs = $filter('colorizeLogs');
  }));

  it('should return the input prefixed with "colorizeLogs filter:"', function () {
    var text = 'angularjs';
    expect(colorizeLogs(text)).toBe('colorizeLogs filter: ' + text);
  });

});
