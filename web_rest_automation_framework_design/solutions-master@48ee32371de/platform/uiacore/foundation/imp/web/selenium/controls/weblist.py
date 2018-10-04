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

from selenium.webdriver.support.select import Select

from uiacore.foundation.interface.patterns import ISelection
from .webelement import WebElement


class WebList(WebElement, ISelection):
    def __init__(self, parent=None, **criteria):
        WebElement.__init__(self, parent, **criteria)
        self._list = None

    def select(self, index=None, by_value='', by_visible_text=''):
        if not self.exists():
            raise RuntimeError('Failed to locate the combobox')

        if index:
            self._list.select_by_index(index)
        elif by_value.strip():
            self._list.select_by_value(by_value.strip())
        elif by_visible_text.strip():
            self._list.select_by_visible_text(by_visible_text.strip())
        else:
            raise ValueError('The identifier is not specified')

    def items(self):
        __selection_items = []
        if self.exists():
            __selection_items = self._list.options

        return __selection_items

    @property
    def current(self):
        if super(WebList, self).current:
            self._list = Select(self._current)

        return self._current

    @property
    def can_select_multiple(self):
        if self.exists():
            return self.object.is_multiple

        return False
