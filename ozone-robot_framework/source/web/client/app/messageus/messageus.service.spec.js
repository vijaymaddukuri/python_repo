'use strict';

describe('Service: messageus', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var messageus;
  beforeEach(inject(function (_messageus_) {
    messageus = _messageus_;
  }));

  it('should do something', function () {
    expect(!!messageus).toBe(true);
  });

});
