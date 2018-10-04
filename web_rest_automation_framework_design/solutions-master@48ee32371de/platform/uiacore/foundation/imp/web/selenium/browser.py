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

import os
import sys

from selenium import webdriver

from support import SmartWait
from uiacore.foundation.interface.web import IBrowser


class SeleniumBrowser(IBrowser):
    """
    Browser wrapper based on Selenium.WebDriver and connection cache
    Only support Firefox and Chrome browsers for the time being
    """

    BINARY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    BROWSER_NAMES = {'ff': '_make_ff',
                     'firefox': '_make_ff',
                     'googlechrome': '_make_chrome',
                     'gc': '_make_chrome',
                     'chrome': '_make_chrome'}

    def __init__(self, browser='Firefox', name=None, wait_time_in_secs=30):
        super(SeleniumBrowser, self).__init__(browser, name)

        if not str(wait_time_in_secs).isdigit():
            self._implicit_wait = 30
        else:
            self._implicit_wait = wait_time_in_secs

        self._cache.register(self._make_browser(browser))

    def activate(self):
        self._browser.switch_to.window(
            self._browser.current_window_handle)

    def launch(self, url='about:blank'):
        self._browser.get(url)
        SmartWait(self._browser,
                  self._implicit_wait).synchronize_page_loading()

    def maximize(self):
        self._browser.maximize_window()

    def switch_to(self, index_or_alias):
        self._browser = self._cache.switch(index_or_alias)

        return self

    def close(self):
        self._cache.close()

    @property
    def current(self):
        if not (self._browser or self._cache.current):
            raise RuntimeError('No browser is open')

        return self._browser or self._cache.current

    def _make_browser(self, browser_name):
        invoker = getattr(self, SeleniumBrowser.BROWSER_NAMES.get(browser_name.lower()))

        if callable(invoker):
            self._browser = invoker()
            self._browser.get('about:blank')
            self._browser.implicitly_wait(self._implicit_wait)
        else:
            raise RuntimeError('Non-deterministic browser name')

        return self._browser

    def _make_ff(self):
        return webdriver.Firefox()

    def _make_chrome(self):
        _default_driver_dir = '/opt/google/chrome/chromedriver'

        if sys.platform.startswith('linux'):
            if os.path.exists(_default_driver_dir):
                _bin_location = _default_driver_dir
            else:
                _bin_location = os.path.join(
                    SeleniumBrowser.BINARY_DIR, 'webdriver/chromedriver')
        else:
            _bin_location = os.path.join(
                SeleniumBrowser.BINARY_DIR, 'webdriver/chromedriver.exe')

        os.environ['webdriver.chrome.driver'] = _bin_location

        return webdriver.Chrome(_bin_location)
