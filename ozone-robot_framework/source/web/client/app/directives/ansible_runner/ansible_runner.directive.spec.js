'use strict';

describe('Directive: ansibleRunner', function () {

  // load the directive's module and view
  beforeEach(module('ehcOzoneApp'));
  beforeEach(module('app/directives/ansible_runner/ansible_runner.html'));

  var element, scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<ansible-runner></ansible-runner>');
    element = $compile(element)(scope);
    scope.$apply();
    expect(element.text()).toBe('this is the ansibleRunner directive');
  }));
});
