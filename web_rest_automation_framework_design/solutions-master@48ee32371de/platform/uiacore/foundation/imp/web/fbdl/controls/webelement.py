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

from uiacore.foundation.interface.web import IWebElement
from uiacore.foundation.interface.patterns import BasePattern

from ui_framework.model.page import Locator, RootPage, ChildPage
from ui_framework.controller.browser import BrowserManager
from ui_framework.controller.find import Find

from selenium.webdriver.common.by import By


class WebElement(IWebElement, BasePattern):
    def __init__(self, element=None, **condition):
        IWebElement.__init__(self, element)

        self._criteria = condition
        self.control = None
        self.locator = None

        self._find_strategies = {
            'ID': By.ID,
            'NAME': By.NAME,
            'CLASSNAME': By.CLASS_NAME,
            'XPATH': By.XPATH,
            'CSS': By.CSS_SELECTOR,
            'DATA_AID': None #By.TAG_NAME
        }

        if (not element) or (not hasattr(element, 'parent')):
            self._parent = RootPage()

        key = None
        for key, value in condition.iteritems():
            if str.upper(key).strip() in self._find_strategies.keys():
                break

        if key:
            func = getattr(Locator(), key, None)
            if func:
                self.locator = func(condition.get(key))
            else:
                self.locator = Locator()
                self.locator.type = key
                self.locator.value = condition.get(key)
                # raise NotImplementedError(
                #         '{} function is not implemented in Locator class'.format(key))
        else:
            raise KeyError('The specified criteria are not supported')

        if self.locator:
            self.control = self.__initialize__(self.locator, self._parent)

        if not self.control:
            raise RuntimeError(
                'Failed to find the element with the type:{0}'.format(self.locator.type))

    def __initialize__(self, locator, parent):
        return ChildPage(locator, parent)

    def exists(self, timeout=30):
        try:
            BrowserManager().wait_for_asynchronous_action_complete(timeout)
        except:
            pass

        if self.current:
            return self._current.is_displayed()

        return False

    @property
    def current(self):
        #Find the element by using the method offered by ui_framework first
        if self._criteria:
            # Refresh the current element
            self._current = None

            try:
                if 'css' not in self._criteria:
                    try:
                        xpath = Find().find_element(self.control)
                        self.__find_element_by_xpath(xpath)
                    except:
                        pass

                if self._current is None:
                    #Alternative way - Find element by using WebDriver's strategies
                    self.__find_element_with_strategies(**self._criteria)

                if isinstance(self._current, list):
                    self._current = self._current[0]
            except:
                pass

        return self._current

    def __find_element_by_xpath(self, xpath):
        self._current = BrowserManager()\
            .get_current_browser().find_element_by_xpath(xpath)

    def __find_element_with_strategies(self, **criteria):
        for key, value in criteria.iteritems():
            key = str.upper(key).strip()

            if key in self._find_strategies.keys():
                self._current = BrowserManager()\
                    .get_current_browser().find_element(
                        by=self._find_strategies.get(key), value=value)

                if self._current:
                    break
        else:
            raise KeyError(
                    'The specified criteria {} are not supported'.format(**criteria))
