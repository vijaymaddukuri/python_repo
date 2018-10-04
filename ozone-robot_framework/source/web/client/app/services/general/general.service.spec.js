'use strict';

describe('Service: general', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var general;
  beforeEach(inject(function (_general_) {
    general = _general_;
  }));

  it('should do something', function () {
    expect(!!general).toBe(true);
  });

});
