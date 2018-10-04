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

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from uiacore.foundation.utils import ConnectionCache


class SmartWait(object):
    def __init__(self, driver=None, timeout_in_secs=30.0, poll_frequency=1.0):
        """
        Customized wait based on WebDriverWait
        :param driver: WebDriver instance
        :param timeout_in_secs: timeout
        :param poll_frequency: sleep interval in seconds between calls
        """
        self._driver = driver or ConnectionCache().current

        try:
            timeout_in_secs = float(timeout_in_secs)
            poll_frequency = float(poll_frequency)
        except:
            timeout_in_secs = 30.0
            poll_frequency = 1.0

        self._timeout_in_secs = timeout_in_secs
        self._poll = poll_frequency

    def synchronize_page_loading(self):
        """
        Waits until the whole page has fully loaded.

        Fails if `timeout_in_secs` expires before the element is enabled. See
        `introduction` for more information about `timeout_in_secs` and its
        default value.
        """

        try:
            WebDriverWait(
                self._driver, self._timeout_in_secs, self._poll
            ).until(lambda s: s.execute_script(
                'return document.readyState=="complete";'),
                    'Fail to wait until page full loaded in {} seconds'.format(
                        self._timeout_in_secs))
        except TimeoutException as ex:
            raise ex

    def synchronize_animations(self):
        """
        Waits until the asynchronous ajax animation complete

        Fails if `timeout_in_secs` expires before the element is enabled. See
        `introduction` for more information about `timeout_in_secs` and its
        default value.
        """

        xmlhttp_animation_script = 'return (window.xmlhttp.readyState == 4 && window.xmlhttp.status == 200);'
        jquery_animation_script = 'return (window.jQuery.active==0);'
        prototype_animation_script = 'return (window.Ajax.activeRequestCount==0);'
        dojo_animation_script = 'return (window.dojo.io.XMLHTTPTransport.inFlight.length==0);'
        angular_animation_script = 'return window.angular.element(document.body)' \
                                   '.injector().get("$http").pendingRequests.length==0;'

        animation_script_pairs = {
            'xmlhttp': xmlhttp_animation_script,
            'jQuery': jquery_animation_script,
            'Ajax': prototype_animation_script,
            'dojo': dojo_animation_script,
            'angular': angular_animation_script}

        for key, value in animation_script_pairs.iteritems():
            result = bool(self._driver.execute_script(
                'if(window.{}) return true; else return false;'.format(key)))

            if result:
                try:
                    WebDriverWait(
                        self._driver, self._timeout_in_secs, self._poll
                    ).until(
                        lambda exp: exp.execute_script(value),
                        'Fail to wait until animation complete in {} seconds'.format(
                            self._timeout_in_secs))
                except TimeoutException as ex:
                    raise ex
