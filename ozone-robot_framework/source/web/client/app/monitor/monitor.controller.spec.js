'use strict';

describe('Component: MonitorComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var MonitorComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    MonitorComponent = $componentController('MonitorComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
