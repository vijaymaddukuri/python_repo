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
from uiacore.foundation.interface.patterns import IValue, IText


class WebEdit(WebElement, IValue, IText):
    def __init__(self, parent=None, **criteria):
        WebElement.__init__(self, **criteria)

        if parent:
            self._parent = parent

    def set(self, value=None):
        if not self.exists():
            raise RuntimeError('WebEdit control is not displayed')

        self.object.clear()
        self.object.send_keys(value)

    @property
    def value(self):
        if self.exists():
            return self.object.text

        return None

    @property
    def is_read_only(self):
        if self.exists():
            return not self.object.is_enabled()

        return False
