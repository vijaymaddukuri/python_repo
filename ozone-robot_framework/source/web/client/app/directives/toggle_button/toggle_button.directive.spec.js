'use strict';

describe('Directive: toggleButton', function () {

  // load the directive's module and view
  beforeEach(module('ehcOzoneApp'));
  beforeEach(module('app/directives/toggle_button/toggle_button.html'));

  var element, scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<toggle-button></toggle-button>');
    element = $compile(element)(scope);
    scope.$apply();
    expect(element.text()).toBe('this is the toggleButton directive');
  }));
});
