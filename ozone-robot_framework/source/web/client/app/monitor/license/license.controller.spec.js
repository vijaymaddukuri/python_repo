'use strict';

describe('Component: LicenseComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var LicenseComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    LicenseComponent = $componentController('LicenseComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
