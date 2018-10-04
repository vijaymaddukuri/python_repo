'use strict';

describe('Directive: customDataTable', function () {

  // load the directive's module and view
  beforeEach(module('ehcOzoneApp'));
  beforeEach(module('app/directives/custom_data_table/custom_data_table.html'));

  var element, scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<custom-data-table></custom-data-table>');
    element = $compile(element)(scope);
    scope.$apply();
    expect(element.text()).toBe('this is the customDataTable directive');
  }));
});
