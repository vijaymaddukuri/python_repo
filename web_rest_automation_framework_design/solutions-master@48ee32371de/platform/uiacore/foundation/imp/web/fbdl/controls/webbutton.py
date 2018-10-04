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
from uiacore.foundation.interface.patterns import IInvoke
from ui_framework.model.button import Button


class WebButton(WebElement, IInvoke):
    def __init__(self, parent=None, **condition):
        WebElement.__init__(self, parent, **condition)

    def __initialize__(self, locator, parent):
        return Button(locator, parent)

    def click(self):
        self.current.click()

    @property
    def enabled(self):
        if self.current:
            return self._current.is_displayed() and \
                   self._current.is_enabled()

        return False
