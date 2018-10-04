'use strict';

describe('Component: ViewProjectComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var ViewProjectComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    ViewProjectComponent = $componentController('ViewProjectComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
