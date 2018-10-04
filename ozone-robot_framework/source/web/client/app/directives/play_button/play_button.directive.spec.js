'use strict';

describe('Directive: playButton', function () {

  // load the directive's module and view
  beforeEach(module('ehcOzoneApp'));
  beforeEach(module('app/directives/play_button/play_button.html'));

  var element, scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<play-button></play-button>');
    element = $compile(element)(scope);
    scope.$apply();
    expect(element.text()).toBe('this is the playButton directive');
  }));
});
