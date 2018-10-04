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

from ehc_e2e.utils.context import DataContext

from ehc_e2e.auc import (LaunchBrowser, CloseBrowser)


class BaseWorkflow(object):
    def __init__(self, ctx=None):
        self._GC_TAG = 'GC'
        self._WORKFLOW_TAG = 'WORKFLOW'

        if not ctx or not hasattr(ctx, self._GC_TAG):
            self.ctx = DataContext(None, self._GC_TAG)
            self.ctx.update_context(None, self._WORKFLOW_TAG)

        self.wf_context = getattr(self.ctx, self._WORKFLOW_TAG)
        self.gc_context = getattr(self.ctx, self._GC_TAG)

    def apply_settings_from_files(self, global_file, *workflow_files):
        self.ctx.update_context(global_file, self._GC_TAG)

        for yaml_file in workflow_files:
            self.ctx.update_context(yaml_file, self._WORKFLOW_TAG)

    def reset_settings(self):
        self.wf_context = None
        self.gc_context = None
        self.ctx = None

    def user_opens_browser(self, browser_type=None, base_url=None):
        self.wf_context.launch_browser.browserType = (
            browser_type or self.wf_context.launch_browser.browserType)
        self.wf_context.launch_browser.baseUrl = (
            base_url or self.wf_context.launch_browser.baseUrl)

        LaunchBrowser(
            self.user_opens_browser.__name__,
            ctx_in=self.wf_context.launch_browser,
            ctx_out=self.wf_context.shared.current_browser,
        ).run()

    def user_closes_browser(self):
        if not self.wf_context.shared.current_browser.instance:
            return

        CloseBrowser(
            self.user_closes_browser.__name__,
            ctx_in=self.wf_context.shared.current_browser,
            ctx_out=self.wf_context.shared.current_browser
        ).run()
