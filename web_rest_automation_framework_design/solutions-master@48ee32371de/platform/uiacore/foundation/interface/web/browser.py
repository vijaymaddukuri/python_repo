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

from uiacore.foundation.interface import ApplicationUnderTest
from uiacore.foundation.utils import ConnectionCache


class IBrowser(ApplicationUnderTest):
    def __init__(self, browser='Firefox', name=None):
        self._browser = None
        self._cache = ConnectionCache(name)
        self.__type = browser

        if name:
            self.__name = name

    def launch(self, url='about:blank'):
        pass

    # def navigate(self, url=None):
    #     self.launch(url)

    def maximize(self):
        pass

    def close(self):
        pass
