'use strict';

describe('Controller: RevertAllCtrl', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var RevertAllCtrl, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    RevertAllCtrl = $controller('RevertAllCtrl', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
