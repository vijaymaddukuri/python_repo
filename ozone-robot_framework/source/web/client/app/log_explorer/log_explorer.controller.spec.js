'use strict';

describe('Component: LogExplorerComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var LogExplorerComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    LogExplorerComponent = $componentController('LogExplorerComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
