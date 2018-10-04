'use strict';

describe('Directive: logViewer', function () {

  // load the directive's module and view
  beforeEach(module('ehcOzoneApp'));
  beforeEach(module('app/directives/log_viewer/log_viewer.html'));

  var element, scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<log-viewer></log-viewer>');
    element = $compile(element)(scope);
    scope.$apply();
    expect(element.text()).toBe('this is the logViewer directive');
  }));
});
