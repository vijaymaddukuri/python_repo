#  Copyright 2016 EMC GSE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

from uiacore.foundation.imp.web.selenium.support import SmartWait
from uiacore.foundation.interface.patterns import BasePattern
from uiacore.foundation.interface.web import IWebElement
from .webpage import WebPage


class WebElement(IWebElement, BasePattern):
    find_strategies = {
            'ID': 'find_elements_by_id',
            'NAME': 'find_elements_by_name',
            'CLASSNAME': 'find_elements_by_name',
            'XPATH': 'find_elements_by_xpath',
            'CSS': 'find_elements_by_css_selector',
            'TAG': 'find_elements_by_tag_name',
        }

    def __init__(self, element=None, **criteria):
        IWebElement.__init__(self, element or WebPage())
        self._locators = None

        if not self._current:
            if element and isinstance(element, SeleniumWebElement):
                self._current = element
            elif not criteria:
                raise ValueError('Unable to initialize the WebElement')
            else:
                self._locators = self._parse_criteria(**criteria)

    def activate(self):
        if self._parent and self.exists():
            self._parent.execute_script(
                    'arguments[0].focus();', self.object)

    def exists(self, timeout_in_secs=30):
        try:
            SmartWait(self._parent, timeout_in_secs).synchronize_animations()
        except:
            pass

        return self.object.is_displayed() if self.current else False

    @property
    def object(self):
        """
        Test Object in Memory (Not refreshed)
        :return: WebElement
        """
        return self._current or self.current

    @property
    def current(self):
        """
        Runtime object on web page within specific browser
        :return: WebElement
        """
        # TODO: Refactoring element searching strategies
        if self._locators:
            _elements = self._find_elements()
            self._current = _elements[0] if _elements else None

        return self._current

    def _parse_criteria(self, **criteria):
        locators = []

        for key, value in criteria.iteritems():
            key = str(key).upper().strip()
            value = str(value).strip()
            if key in WebElement.find_strategies:
                locators.append([WebElement.find_strategies.get(key), value])

        if not locators:
            raise ValueError('Non-deterministic locator')

        return locators

    def _find_elements(self):
        _elements = []

        for key, value in self._locators:
            _invoker = None

            if hasattr(self._parent, key):
                _invoker = getattr(self._parent, key)

            if _invoker and callable(_invoker):
                _elements.extend(
                        self._normalize_result(_invoker(value)))

        return _elements

    def _normalize_result(self, elements):
        if hasattr(elements, '__len__') and (
                    elements is not basestring or elements is not str):
            return elements
        else:
            return []
