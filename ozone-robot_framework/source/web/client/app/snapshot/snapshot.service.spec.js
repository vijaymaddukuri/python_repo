'use strict';

describe('Service: snapshot', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var snapshot;
  beforeEach(inject(function (_snapshot_) {
    snapshot = _snapshot_;
  }));

  it('should do something', function () {
    expect(!!snapshot).toBe(true);
  });

});
