'use strict';

describe('Filter: replaceLineBreaks', function () {

  // load the filter's module
  beforeEach(module('ehcOzoneApp'));

  // initialize a new instance of the filter before each test
  var replaceLineBreaks;
  beforeEach(inject(function ($filter) {
    replaceLineBreaks = $filter('replaceLineBreaks');
  }));

  it('should return the input prefixed with "replaceLineBreaks filter:"', function () {
    var text = 'angularjs';
    expect(replaceLineBreaks(text)).toBe('replaceLineBreaks filter: ' + text);
  });

});
