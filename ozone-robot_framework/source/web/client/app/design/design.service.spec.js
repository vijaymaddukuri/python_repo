'use strict';

describe('Service: design', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var design;
  beforeEach(inject(function (_design_) {
    design = _design_;
  }));

  it('should do something', function () {
    expect(!!design).toBe(true);
  });

});
