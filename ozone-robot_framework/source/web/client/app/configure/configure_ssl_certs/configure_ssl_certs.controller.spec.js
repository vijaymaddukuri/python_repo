'use strict';

describe('Component: ConfigureSslCertsComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var ConfigureSslCertsComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    ConfigureSslCertsComponent = $componentController('ConfigureSslCertsComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
