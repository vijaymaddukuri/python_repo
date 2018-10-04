'use strict';

describe('Directive: statusLabel', function () {

  // load the directive's module and view
  beforeEach(module('ehcOzoneApp'));
  beforeEach(module('app/directives/status_label/status_label.html'));

  var element, scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<status-label></status-label>');
    element = $compile(element)(scope);
    scope.$apply();
    expect(element.text()).toBe('this is the statusLabel directive');
  }));
});
