'use strict';

describe('Component: LastGoodConfigurationsComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var LastGoodConfigurationsComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    LastGoodConfigurationsComponent = $componentController('LastGoodConfigurationsComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
