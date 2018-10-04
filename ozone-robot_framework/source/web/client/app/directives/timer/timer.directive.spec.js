'use strict';

describe('Directive: timer', function () {

  // load the directive's module and view
  beforeEach(module('ehcOzoneApp'));
  beforeEach(module('app/directives/timer/timer.html'));

  var element, scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<timer></timer>');
    element = $compile(element)(scope);
    scope.$apply();
    expect(element.text()).toBe('this is the timer directive');
  }));
});
