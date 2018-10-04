'use strict';

describe('Service: configure', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var configure;
  beforeEach(inject(function (_configure_) {
    configure = _configure_;
  }));

  it('should do something', function () {
    expect(!!configure).toBe(true);
  });

});
