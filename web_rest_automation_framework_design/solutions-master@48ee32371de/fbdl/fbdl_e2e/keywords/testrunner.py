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

import unittest

from fbdl_e2e.auc import \
    OpenBrowser, CloseBrowser, \
    LoginGlobalUI, LogoutGlobalUI, \
    CreateWorkSpace, AccessWorkspace, \
    DeployServices, DeployTools, \
    SearchTools, SearchDataSets, \
    PublishTools, PublishDataSets, \
    DeleteWorkspace, DeleteRegisteredWorkingSets,\
    ViewQuota,RetrieveWorkBenchVM,DeleteDataSets,\
    RegisterTemplate, SubmitAsset, SubmitTemplate, AcceptTemplate,\
    AddDataSetsTags,RegisterAsset,AcceptAsset,\
    DeployDataSets,AddAsset,AddCollaborators,ValidateUserPermission, \
    DeleteCollaborators, DeleteDeployedWorkingSets
from fbdl_e2e.workflow.context import Context


class UTMain(unittest.TestCase):
    def setUp(self):
        import os
        _cd = os.path.dirname(os.path.realpath(__file__))
        _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
        _yaml_file = os.path.join(_parent_dir, 'config/config_pie.yaml')
        _workflow_yaml_file = os.path.join(_parent_dir, 'config/E2EWF-2.config.yaml')
        _asset_yaml_file = os.path.join(_parent_dir, 'config/test_config.yaml')
        Context.load(_yaml_file,[_asset_yaml_file, _workflow_yaml_file])

    def tearDown(self):
        pass

    def test_AUCs(self):
        OpenBrowser().run()

        LoginGlobalUI().run()
        CreateWorkSpace().run()
        AccessWorkspace().run()

        ViewQuota().run()
        RetrieveWorkBenchVM().run()
        AddAsset().run()
        RegisterAsset().run()
        PublishDataSets().run()
        AcceptAsset().run()
        LogoutGlobalUI().run()
        LoginGlobalUI().run()
        AccessWorkspace().run()
        SearchDataSets().run()
        DeleteDataSets().run()
        DeleteDataSets().run()
        SearchTools().run()
        DeployServices().run()
        AccessWorkspace().run()
        DeployTools().run()
        SearchDataSets().run()
        PublishTools().run()
        PublishDataSets().run()
        DeleteWorkspace().run()
        DeleteRegisteredWorkingSets().run()
        LogoutGlobalUI().run()

        CloseBrowser().run()

    def test_Workflows(self):

        OpenBrowser().run()

        LoginGlobalUI().run()
        # CreateWorkSpace().run()
        AccessWorkspace().run()
        # RetrieveWorkBenchVM().run()
        AddAsset().run()
        RegisterAsset().run()
        #
        # PublishTools().run()
        PublishDataSets().run()
        AcceptAsset().run()
        AddDataSetsTags().run()

        DeleteRegisteredWorkingSets().run()
        LogoutGlobalUI().run()
        #
        #
        LoginGlobalUI().run()
        # CreateWorkSpace().run()
        AccessWorkspace().run()
        # RetrieveWorkBenchVM().run()
        # DeployTools().run()

        SearchDataSets().run()
        DeployDataSets().run()

        DeleteDeployedWorkingSets().run()
        LogoutGlobalUI().run()

        # LoginGlobalUI().run()
        # AccessWorkspace().run()
        # DeleteWorkspace().run()
        # LogoutGlobalUI().run()

        CloseBrowser().run()

    def test_cli(self):

        OpenBrowser().run()

        LoginGlobalUI().run()
        # CreateWorkSpace().run()
        AccessWorkspace().run()
        AddAsset().run()

    def test_permission(self):
        OpenBrowser().run()

        # LoginGlobalUI().run()
        # CreateWorkSpace().run()
        # ViewQuota().run()
        # AccessWorkspace().run()
        # ValidateUserPermission().run()
        # AddCollaborators().run()
        # LogoutGlobalUI().run()
        #
        #
        # LoginGlobalUI().run()
        # AccessWorkspace().run()
        # ValidateUserPermission().run()
        # DeployServices().run()
        # LogoutGlobalUI().run()
        #
        # LoginGlobalUI().run()
        # AccessWorkspace().run()
        # DeleteCollaborators().run()
        # LogoutGlobalUI().run()
        #
        # LoginGlobalUI().run()
        # AccessWorkspace().run()
        # DeployServices().run()
        # LogoutGlobalUI().run()

        LoginGlobalUI().run()
        DeleteWorkspace().run()
        LogoutGlobalUI().run()

        CloseBrowser().run()


    def test_tools(self):

        OpenBrowser().run()

        LoginGlobalUI().run()
        # CreateWorkSpace().run()
        AccessWorkspace().run()
        RetrieveWorkBenchVM().run()
        AddAsset().run()
        RegisterAsset().run()
        PublishTools().run()
        AcceptAsset().run()
        LogoutGlobalUI().run()


        LoginGlobalUI().run()
        # CreateWorkSpace().run()
        AccessWorkspace().run()
        SearchTools().run()
        DeployTools().run()
        LogoutGlobalUI().run()

        # LoginGlobalUI().run()
        # AccessWorkspace().run()
        # DeleteWorkspace().run()
        # LogoutGlobalUI().run()

        CloseBrowser().run()
        
if __name__ == "__main__":
    unittest.main()