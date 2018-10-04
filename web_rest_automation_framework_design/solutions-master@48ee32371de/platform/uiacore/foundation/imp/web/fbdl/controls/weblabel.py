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
from uiacore.foundation.interface.patterns import IText

from ui_framework.model.label import Label


class WebLabel(WebElement, IText):
    def __init__(self, parent=None, **condition):
        super(WebLabel, self).__init__(parent, **condition)

    def __initialize__(self, locator, parent):
        return Label(locator, parent)

    @property
    def value(self):
        if self.current:
            return self._current.text

        return None
