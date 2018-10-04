'use strict';

describe('Service: tile', function () {

  // load the service's module
  beforeEach(module('ehcOzoneApp'));

  // instantiate service
  var tile;
  beforeEach(inject(function (_tile_) {
    tile = _tile_;
  }));

  it('should do something', function () {
    expect(!!tile).toBe(true);
  });

});
