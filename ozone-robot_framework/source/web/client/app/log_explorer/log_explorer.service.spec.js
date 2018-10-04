'use strict';

describe('Service: logExplorer', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var logExplorer;
  beforeEach(inject(function (_logExplorer_) {
    logExplorer = _logExplorer_;
  }));

  it('should do something', function () {
    expect(!!logExplorer).toBe(true);
  });

});
