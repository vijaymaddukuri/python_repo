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


class IElement(object):
    def __init__(self, element=None):
        self._parent = None
        self._current = None

        if element:
            if hasattr(element, 'parent'):
                self._parent = element.parent

            if hasattr(element, 'current'):
                self._current = element.current

    @property
    def current(self):
        return self._current

    @property
    def parent(self):
        return self._parent
