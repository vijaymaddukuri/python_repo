'use strict';

describe('Service: ansible', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var ansible;
  beforeEach(inject(function (_ansible_) {
    ansible = _ansible_;
  }));

  it('should do something', function () {
    expect(!!ansible).toBe(true);
  });

});
