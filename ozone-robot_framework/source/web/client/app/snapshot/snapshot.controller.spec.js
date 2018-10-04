'use strict';

describe('Component: SnapshotComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var SnapshotComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    SnapshotComponent = $componentController('SnapshotComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
