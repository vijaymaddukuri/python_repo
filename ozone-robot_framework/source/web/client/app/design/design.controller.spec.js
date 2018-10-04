'use strict';

describe('Component: DesignComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var DesignComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    DesignComponent = $componentController('DesignComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
