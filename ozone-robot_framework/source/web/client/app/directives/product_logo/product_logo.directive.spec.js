'use strict';

describe('Directive: productLogo', function () {

  // load the directive's module and view
  beforeEach(module('ehcOzoneApp'));
  beforeEach(module('app/directives/product_logo/product_logo.html'));

  var element, scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<product-logo></product-logo>');
    element = $compile(element)(scope);
    scope.$apply();
    expect(element.text()).toBe('this is the productLogo directive');
  }));
});
