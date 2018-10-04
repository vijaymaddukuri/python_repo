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

from uiacore.foundation.factory.web import ITech
from uiacore.foundation.imp.web.fbdl.browser import FBDLBrowser
from uiacore.foundation.imp.web.fbdl.controls import (
    WebElement, WebButton, WebLink, WebCombo, WebLabel, WebTextBox)
from uiacore.foundation.interface.patterns import (
    BasePattern, IInvoke, ILink, ISelection, IText, IValue)


class FBDLTech(ITech):
    def get_browser(self):
        return FBDLBrowser

    def get_element_type(self, pattern):
        _element_pattern_pairs = {
            BasePattern: WebElement,
            IValue: WebTextBox,
            IInvoke: WebButton,
            IText: WebLabel,
            ILink: WebLink,
            ISelection: WebCombo
        }

        _type = _element_pattern_pairs.get(pattern, None)

        if _type is None:
            raise NotImplementedError(
                'The {} is not implemented'.format(pattern))

        return _type
