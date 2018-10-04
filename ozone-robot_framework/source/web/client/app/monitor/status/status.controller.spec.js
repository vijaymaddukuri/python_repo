'use strict';

describe('Component: StatusComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var StatusComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    StatusComponent = $componentController('StatusComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
