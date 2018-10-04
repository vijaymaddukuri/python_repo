'use strict';

describe('Service: upgrade', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var upgrade;
  beforeEach(inject(function (_upgrade_) {
    upgrade = _upgrade_;
  }));

  it('should do something', function () {
    expect(!!upgrade).toBe(true);
  });

});
