'use strict';

describe('Component: VersionsComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var VersionsComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    VersionsComponent = $componentController('VersionsComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
