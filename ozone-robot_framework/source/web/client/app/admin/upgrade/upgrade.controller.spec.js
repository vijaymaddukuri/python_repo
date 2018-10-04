'use strict';

describe('Component: UpgradeComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var UpgradeComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    UpgradeComponent = $componentController('UpgradeComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
