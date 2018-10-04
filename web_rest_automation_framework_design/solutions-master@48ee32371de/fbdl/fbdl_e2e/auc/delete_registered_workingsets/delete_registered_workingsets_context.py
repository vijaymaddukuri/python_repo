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
from fbdl_e2e.workflow.context import Context


class DeleteRegisteredWorkingSetsContext(Context):
    @staticmethod
    def validate():
        __extended_variables_to_validate = ['current_browser', 'is_login', 'created_workspace_names']
        return Context.validate(__extended_variables_to_validate)
