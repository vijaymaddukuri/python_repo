'use strict';

describe('Component: ImportComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var ImportComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    ImportComponent = $componentController('ImportComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
