'use strict';

describe('Filter: humanizeText', function () {

  // load the filter's module
  beforeEach(module('ehcOzoneApp'));

  // initialize a new instance of the filter before each test
  var humanizeText;
  beforeEach(inject(function ($filter) {
    humanizeText = $filter('humanizeText');
  }));

  it('should return the input prefixed with "humanizeText filter:"', function () {
    var text = 'angularjs';
    expect(humanizeText(text)).toBe('humanizeText filter: ' + text);
  });

});
