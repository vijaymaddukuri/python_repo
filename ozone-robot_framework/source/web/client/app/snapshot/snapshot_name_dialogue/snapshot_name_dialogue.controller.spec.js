'use strict';

describe('Controller: SnapshotNameDialogueCtrl', function () {

  // load the controller's module
  beforeEach(module('ehcOzoneApp'));

  var SnapshotNameDialogueCtrl, scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SnapshotNameDialogueCtrl = $controller('SnapshotNameDialogueCtrl', {
      $scope: scope
    });
  }));

  it('should ...', function () {
    expect(1).toEqual(1);
  });
});
