'use strict';

describe('Controller: MessageusCtrl', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var MessageusCtrl, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MessageusCtrl = $controller('MessageusCtrl', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
