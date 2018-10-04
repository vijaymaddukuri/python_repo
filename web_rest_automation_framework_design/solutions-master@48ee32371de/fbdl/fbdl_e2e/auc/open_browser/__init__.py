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

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.open_browser.open_browser_context import OpenBrowserContext
from fbdl_e2e.workflow.context import Context
from uiacore.modeling.webui.browser import *
from robot.api import logger


class OpenBrowser(BaseUseCase):
    """
    Data scientist opens web browser
    """
    def test_open_browser(self):
        logger.info('Data scientist opens web browser...', False, False)
        self.browser = Browser(browser='Chrome', name='globalUI')
        self.browser.launch(Context.get('global_ui_address'))
        self.browser.maximize()

        Context.set('current_browser', self.browser)

    def setUp(self):
        OpenBrowserContext.validate()

    def runTest(self):
        self.test_open_browser()
