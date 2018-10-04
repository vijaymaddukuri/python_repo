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

from .webelement import WebElement
from uiacore.foundation.interface.patterns import ISelection

from selenium.webdriver.support.select import Select


class WebCombo(WebElement, ISelection):
    def __init__(self, parent=None, **condition):
        WebElement.__init__(self, parent, **condition)

    def select(self, index=None, by_value='', by_visible_text=''):
        if not self.current:
            raise RuntimeError('Failed to locate the combobox')

        if index:
            self._current.select_by_index(index)
        elif by_value.strip():
            self._current.select_by_value(by_value.strip())
        elif by_visible_text.strip():
            self._current.select_by_visible_text(by_visible_text.strip())
        else:
            raise ValueError('The identifier is not specified')

    def items(self):
        __selection_items = []
        if self.current:
            __selection_items = self._current.options

        return __selection_items

    @property
    def current(self):
        if super(WebCombo, self).current:
            self._current = Select(self._current)

        return self._current

    @property
    def can_select_multiple(self):
        if self.current:
            return self._current.is_multiple

        return False
