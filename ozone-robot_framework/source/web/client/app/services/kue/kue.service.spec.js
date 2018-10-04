'use strict';

describe('Service: kue', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var kue;
  beforeEach(inject(function (_kue_) {
    kue = _kue_;
  }));

  it('should do something', function () {
    expect(!!kue).toBe(true);
  });

});
