'use strict';

describe('Component: AnsibleComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var AnsibleComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    AnsibleComponent = $componentController('AnsibleComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
