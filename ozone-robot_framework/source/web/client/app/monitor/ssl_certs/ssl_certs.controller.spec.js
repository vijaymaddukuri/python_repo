'use strict';

describe('Component: SslCertsComponent', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var SslCertsComponent, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($componentController, $rootScope) {
    scope = $rootScope.$new();
    SslCertsComponent = $componentController('SslCertsComponent', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
