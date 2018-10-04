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

from auc.executable.baseusecase import BaseUseCase
from uiacore.modeling.webui.browser import Browser


class LaunchBrowser(BaseUseCase):
    """
    Launch browser and navigate to the specified URL
    """

    def test_launch_browser(self):
        self.browser = Browser(self.ctx_in.browserType, name='EHC_UI')
        self.browser.launch(self.ctx_in.baseUrl)
        self.browser.maximize()

    def runTest(self):
        self.test_launch_browser()

    def _validate_context(self):
        self.browser = None

        if self.ctx_in:
            assert self.ctx_in.browserType is not None
            assert self.ctx_in.baseUrl is not None

    def _finalize_context(self):
        setattr(self.ctx_out, 'instance', self.browser)
