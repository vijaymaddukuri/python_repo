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

from uiacore.foundation.interface.patterns import IFrame
from .webelement import WebElement


class Frame(WebElement, IFrame):
    def __init__(self, parent=None, **criteria):
        WebElement.__init__(self, **{'tag': 'iframe'})
        self._constraints = criteria

        if parent:
            self._parent = parent

    def activate(self):
        if self._parent and self.exists():
            self._parent.switch_to.frame(self.object)

    def deactivate(self):
        if self._parent:
            self._parent.switch_to.default_content()

    @property
    def current(self):
        if self._locators:
            self._current = None

            _elements = self._find_elements()

            # Tricky part for filtering out frames
            # It should be done within super class
            for element in _elements:
                for key, value in self._constraints.iteritems():
                    if element.get_attribute(key) != value:
                        break
                else:
                    self._current = element
                    break

        return self._current

    @property
    def title(self):
        self.deactivate()

        if self.exists():
            return self.object.get_attribute('title')

        return None
