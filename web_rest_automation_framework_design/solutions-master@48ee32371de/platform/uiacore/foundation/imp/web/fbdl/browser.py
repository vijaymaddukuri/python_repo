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

from uiacore.foundation.interface.web import IBrowser

from ui_framework.controller import Browser


class FBDLBrowser(IBrowser):
    def __init__(self, browser='Firefox', name=None, wait_time_in_secs=30):
        super(FBDLBrowser, self).__init__(browser, name)

        if not str(wait_time_in_secs).isdigit():
            self._implicit_wait = 30
        else:
            self._implicit_wait = wait_time_in_secs

        self._browser = Browser()
        self._browser.launch_browser(
            url='about:blank', browser=browser, alias=name)

        self._browser.get_current_browser()\
            .implicitly_wait(self._implicit_wait)

    def launch(self, url='about:blank'):
        self._browser.go_to(url)
        self._browser.wait_for_page_loading(
            timeout=self._implicit_wait)

    def maximize(self):
        self._browser.get_current_browser().maximize_window()

    def close(self):
        self._browser.close_browser()
