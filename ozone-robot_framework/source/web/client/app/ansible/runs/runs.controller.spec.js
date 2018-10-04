'use strict';

describe('Component: RunsComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var RunsComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    RunsComponent = $componentController('RunsComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
