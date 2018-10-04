'use strict';

describe('Service: mdescape', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var mdescape;
  beforeEach(inject(function (_mdescape_) {
    mdescape = _mdescape_;
  }));

  it('should do something', function () {
    expect(!!mdescape).toBe(true);
  });

});
