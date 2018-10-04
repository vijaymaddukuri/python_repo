'use strict';

describe('Component: SystemComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var SystemComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    SystemComponent = $componentController('SystemComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
