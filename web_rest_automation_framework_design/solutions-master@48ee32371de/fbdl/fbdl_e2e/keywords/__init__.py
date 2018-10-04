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

from fbdl_e2e.auc import (
    AcceptAsset, AcceptTemplate, AccessWorkspace,
    AddAsset, AddCollaborators, AddDataSetsTags, CloseBrowser,
    CreateWorkSpace, DeleteCollaborators, DeleteDataSets,
    DeleteToolsFromDAC, DeleteToolsFromWorkspace,
    DeleteRegisteredWorkingSets, DeleteDeployedWorkingSets, DeleteWorkspace,
    DeployDataSets, DeployServices,
    DeployTools, LoginGlobalUI, LogoutGlobalUI,
    OpenBrowser, PublishTools, PublishDataSets,
    RegisterAsset, RegisterTemplate,
    RejectAsset, RejectTemplate, RetrieveWorkBenchVM,
    SearchDataSets, SearchTools, SubmitAsset, SubmitTemplate,
    ValidateDeployedDataset, ValidateUserPermission,
    ViewDetailsOfDeployedTool, ViewQuota, CleanUp)

from fbdl_e2e.workflow.context import Context


def load_configurations(global_config_file, *extended_config_files):
    Context.load(global_config_file, extended_config_files)

def clean_up_environment():
    CleanUp(
        name=clean_up_environment.func_name
    ).run()

def print_context():
    Context.print_out()


def data_scientist_opens_browser():
    OpenBrowser(
        name=data_scientist_opens_browser.func_name
    ).run()


def data_scientist_closes_browser():
    CloseBrowser(
        name=data_scientist_closes_browser.func_name
    ).run()


def data_scientist_logs_in_to_global_ui():
    LoginGlobalUI(
        name=data_scientist_logs_in_to_global_ui.func_name
    ).run()


def data_scientist_adds_asset_to_workbench_VM():
    AddAsset(
        name=data_scientist_adds_asset_to_workbench_VM.func_name
    ).run()


def data_scientist_adds_asset_to_cloudera_cluster():
    _cloudera_info = Context.get('cloudera_cluster')
    if _cloudera_info:
        _cloudera_info = _cloudera_info[-1]
        hadoop_dict = {
            'name_node_ip': _cloudera_info.get('Master IP'),
            'user': Context.get('dac_cli_username'),
            'password': Context.get('dac_cli_password'),
            'host': _cloudera_info.get('Namenode Host')
                      }
        Context.set('hadoop_info', hadoop_dict)
        Context.set('add_asset_to_hadoop', True)
    AddAsset(
        name=data_scientist_adds_asset_to_workbench_VM.func_name
    ).run()


def data_scientist_publishes_tools():
    PublishTools(
        name=data_scientist_publishes_tools.func_name
    ).run()


def data_scientist_publishes_datasets():
    PublishDataSets(
        name=data_scientist_publishes_datasets.func_name
    ).run()


def data_scientist_deletes_datasets_from_data_catalog():
    DeleteDataSets(
        name=data_scientist_deletes_datasets_from_data_catalog.func_name
    ).run()


def data_scientist_deletes_registered_workingsets():
    DeleteRegisteredWorkingSets(
        name=data_scientist_deletes_registered_workingsets.func_name
    ).run()


def data_scientist_deletes_deployed_workingsets():
    DeleteDeployedWorkingSets(
        name=data_scientist_deletes_deployed_workingsets.func_name
    ).run()


def data_scientist_logs_out_from_global_ui():
    LogoutGlobalUI(
        name=data_scientist_logs_out_from_global_ui.func_name
    ).run()


def data_scientist_creates_workspace():
    CreateWorkSpace(
        name=data_scientist_creates_workspace.func_name
    ).run()


def data_scientist_deletes_workspace():
    DeleteWorkspace(
        name=data_scientist_deletes_workspace.func_name
    ).run()


def data_scientist_accesses_workspace():
    AccessWorkspace(
        name=data_scientist_accesses_workspace.func_name
    ).run()


def data_scientist_views_quota_information():
    ViewQuota(
        name=data_scientist_views_quota_information.func_name
    ).run()


def data_scientist_retrieve_workbench_VM():
    RetrieveWorkBenchVM(
        name=data_scientist_retrieve_workbench_VM.func_name
    ).run()


def data_scientist_adds_tags_to_datasets():
    AddDataSetsTags(
        name=data_scientist_adds_tags_to_datasets.func_name
    ).run()


def data_scientist_deploys_services():
    DeployServices(
        name=data_scientist_deploys_services.func_name
    ).run()


def data_scientist_deploys_mysql_pcf_service():
    _pcf_mysql_services = Context.get('pcf_mysql_info')

    if _pcf_mysql_services:
        Context.set('services_to_be_deployed', _pcf_mysql_services)

    DeployServices(
        name=data_scientist_deploys_mysql_pcf_service.func_name
    ).run()


def data_scientist_deploys_tools():
    _tools = []
    _accepted_tools = Context.get('accepted_tools')
    if _accepted_tools:
        for tool in _accepted_tools:
            _tool = tool
            _tool['instance'] = 'instance_of_{}'.format(tool['name'])
            _tools.append(_tool)

    Context.set('tools_to_be_deployed', _tools)

    DeployTools(
        name=data_scientist_deploys_tools.func_name
    ).run()


def data_scientist_deploys_cloudera_clusters():
    cloudera_info = Context.get('dac_cloudera_info')
    if cloudera_info:
        Context.set('tools_to_be_deployed', cloudera_info)

    DeployTools(
        name=data_scientist_deploys_cloudera_clusters.func_name
    ).run()

    ViewDetailsOfDeployedTool(
        name='data_scientist_views_deployed_cloudera_cluster'
    ).run()

    Context.set('cloudera_cluster', Context.get('deployed_tools'))


def data_scientist_deploys_hortonworks_clusters():
    hortonworks_info = Context.get('dac_hortonworks_info')
    if hortonworks_info:
        Context.set('tools_to_be_deployed', hortonworks_info)

    DeployTools(
        name=data_scientist_deploys_hortonworks_clusters.func_name
    ).run()

    ViewDetailsOfDeployedTool(
        name='data_scientist_views_deployed_hortonworks_cluster'
    ).run()

    Context.set('hortonworks_cluster', Context.get('deployed_tools'))


def data_scientist_deploys_mongodb_dac_service():
    mongodb_info = Context.get('dac_mongodb_info')

    if mongodb_info:
        Context.set('tools_to_be_deployed', mongodb_info)

    DeployTools(
        name=data_scientist_deploys_mongodb_dac_service.func_name
    ).run()

    ViewDetailsOfDeployedTool(
        name='data_scientist_views_deployed_mongodb_dac_service'
    ).run()

    Context.set('mongodb_dac_service', Context.get('deployed_tools'))


def data_scientist_deploys_datasets():
    DeployDataSets(
        name=data_scientist_deploys_datasets.func_name
    ).run()


def data_scientist_deploys_datasets_to_workbench_vm():
    RetrieveWorkBenchVM(
        name=data_scientist_retrieve_workbench_VM.func_name
    ).run()

    container_info = Context.get('deployed_services')
    container_info = container_info[-1]["instance"]

    _datasets = []
    _accepted_datasets = Context.get('accepted_datasets')
    if _accepted_datasets:
        for _accept in _accepted_datasets:
            from datetime import datetime
            _deploy = {}
            _deploy['name'] = _accept['name']
            _deploy['container'] = container_info
            _deploy['workingset'] = 'ws' + datetime.now().strftime('%y%m%d%H%M')
            # TODO: add other property
            _datasets.append(_deploy)

    Context.set('datasets_to_be_deployed', _datasets)

    DeployDataSets(
        name=data_scientist_deploys_datasets_to_workbench_vm.func_name
    ).run()


def data_scientist_deploys_datasets_to_mysql_pcf():
    container_info = Context.get('deployed_services')or Context.get('pcf_mysql_info')
    container_info = container_info[-1]["instance"]

    _datasets = []
    _accepted_datasets = Context.get('accepted_datasets')
    if _accepted_datasets:
        for _accept in _accepted_datasets:
            from datetime import datetime
            _deploy = {}
            _deploy['name'] = _accept['name']
            _deploy['container'] = container_info
            _deploy['workingset'] = 'ws' + datetime.now().strftime('%y%m%d%H%M')
            # TODO: add other property
            _datasets.append(_deploy)

    Context.set('datasets_to_be_deployed', _datasets)

    DeployDataSets(
        name=data_scientist_deploys_datasets_to_workbench_vm.func_name
    ).run()

    RetrieveWorkBenchVM(
        name='data_scientist_retrieves_workbench_vm_info'
    ).run()

    ValidateDeployedDataset(
        name='data_scientist_validates_deployed_datasets_in_pcf_mysql'
    ).run()


def data_scientist_deploys_datasets_to_cloudera():
    container_info = Context.get('deployed_tools') or Context.get('cloudera_cluster')
    container_info = container_info[-1]["instance"]

    _datasets = []
    _accepted_datasets = Context.get('accepted_datasets')
    if _accepted_datasets:
        for _accept in _accepted_datasets:
            from datetime import datetime
            _deploy = {}
            _deploy['name'] = _accept['name']
            _deploy['container'] = container_info
            _deploy['workingset'] = 'ws' + datetime.now().strftime('%y%m%d%H%M')
            # TODO: add other property
            _datasets.append(_deploy)

    Context.set('datasets_to_be_deployed', _datasets)

    DeployDataSets(
        name=data_scientist_deploys_datasets_to_cloudera.func_name
    ).run()

    RetrieveWorkBenchVM(
        name='data_scientist_retrieves_workbench_vm_info'
    ).run()

    ValidateDeployedDataset(
        name='data_scientist_validates_deployed_datasets_in_cloudera'
    ).run()


def data_scientist_deploys_datasets_to_hortonworks():
    container_info = Context.get('deployed_tools') or Context.get('hortonworks_cluster')
    container_info = container_info[-1]["instance"]

    _datasets = []
    _accepted_datasets = Context.get('accepted_datasets')
    if _accepted_datasets:
        for _accept in _accepted_datasets:
            from datetime import datetime
            _deploy = {}
            _deploy['name'] = _accept['name']
            _deploy['container'] = container_info
            _deploy['workingset'] = 'ws' + datetime.now().strftime('%y%m%d%H%M')
            # TODO: add other property
            _datasets.append(_deploy)

    Context.set('datasets_to_be_deployed', _datasets)

    DeployDataSets(
        name=data_scientist_deploys_datasets_to_hortonworks.func_name
    ).run()

    RetrieveWorkBenchVM(
        name='data_scientist_retrieves_workbench_vm_info'
    ).run()

    ValidateDeployedDataset(
        name='data_scientist_validates_deployed_datasets_in_hortonworks'
    ).run()


def data_scientist_deploys_datasets_to_mongodb_dac():
    container_info = Context.get('deployed_tools') or Context.get('mongodb_dac_service')
    container_info = container_info[-1]["instance"]

    _datasets = []
    _accepted_datasets = Context.get('accepted_datasets')
    if _accepted_datasets:
        for _accept in _accepted_datasets:
            from datetime import datetime
            _deploy = {}
            _deploy['name'] = _accept['name']
            _deploy['container'] = container_info
            _deploy['workingset'] = 'ws' + datetime.now().strftime('%y%m%d%H%M')
            # TODO: add other property
            _datasets.append(_deploy)

    Context.set('datasets_to_be_deployed', _datasets)

    DeployDataSets(
        name=data_scientist_deploys_datasets_to_mongodb_dac.func_name
    ).run()

    RetrieveWorkBenchVM(
        name='data_scientist_retrieves_workbench_vm_info'
    ).run()

    ValidateDeployedDataset(
        name='data_scientist_validates_deployed_datasets_in_mongo_db'
    ).run()


# def data_scientist_validates_deployed_datasets():
#     RetrieveWorkBenchVM(
#         name='data_scientist_retrieves_workbench_vm_info'
#     ).run()
#
#     ValidateDeployedDataset(
#         name=data_scientist_validates_deployed_datasets.func_name
#     ).run()


def data_scientist_deletes_tools_from_dac():
    DeleteToolsFromDAC(
        name=data_scientist_deletes_tools_from_dac.func_name
    ).run()


def data_scientist_deletes_registered_tools():
    _registered_tools = Context.get('accepted_tools')

    if _registered_tools:
        _tools = []
        for tool in _registered_tools:
            _tools.append(tool.get('name'))

        Context.set('tools_to_be_deleted', _tools)

    DeleteToolsFromWorkspace(
        name=data_scientist_deletes_registered_tools.func_name
    ).run()


def data_scientist_deletes_deployed_pcf_instances():
    _deployed_pcf_services = Context.get('deployed_services')

    if _deployed_pcf_services:
        _services = []
        for service in _deployed_pcf_services:
            _services.append(service.get('instance'))

        Context.set('tools_to_be_deleted', _services)

    DeleteToolsFromWorkspace(
        name=data_scientist_deletes_deployed_pcf_instances.func_name
    ).run()


def data_scientist_deletes_deployed_tools():
    _deployed_tools = Context.get('deployed_tools')

    if _deployed_tools:
        _tools = []
        for tool in _deployed_tools:
            _tools.append(tool.get('instance'))

        Context.set('tools_to_be_deleted', _tools)

    DeleteToolsFromWorkspace(
        name=data_scientist_deletes_deployed_tools.func_name
    ).run()


def administrator_adds_collaborators_to_workspace():
    AddCollaborators(
        name=administrator_adds_collaborators_to_workspace.func_name
    ).run()

    # Update workflow context for the followed AUCs
    _added_users = Context.get('added_collaborators')
    if not _added_users:
        _added_users = Context.get('collaborators_to_be_added')

    if Context.get('secondary_user') not in _added_users:
        Context.set('secondary_user', _added_users[-1])


def administrator_deletes_collaborators_within_workspace():
    DeleteCollaborators(
        name=administrator_deletes_collaborators_within_workspace.func_name
    ).run()


def user_validates_permission():
    ValidateUserPermission(
        name=user_validates_permission.func_name
    ).run()


def data_scientist_searches_tools_in_marketplace():
    SearchTools(
        name=data_scientist_searches_tools_in_marketplace.func_name
    ).run()


def data_scientist_searches_hortonworks_in_marketplace():
    _hortonworks_info = Context.get('dac_hortonworks_info')
    if _hortonworks_info:
        _hortonworks_name = _hortonworks_info[-1].get('name')
        _tools_info = {
            'AssetVisibleName': [_hortonworks_name]
        }
        Context.set('search_tools_name', _tools_info)
    SearchTools(
        name=data_scientist_searches_hortonworks_in_marketplace.func_name
    ).run()


def data_scientist_searches_cloudera_in_marketplace():
    _cloudera_info = Context.get('dac_cloudera_info')
    if _cloudera_info:
        _cloudera_name = _cloudera_info[-1].get('name')
        _tools_info = {
            'AssetVisibleName': [_cloudera_name]
        }
        Context.set('search_tools_name', _tools_info)
    SearchTools(
        name=data_scientist_searches_cloudera_in_marketplace.func_name
    ).run()


def data_scientist_searches_mongodb_in_marketplace():
    _mongodb_info = Context.get('dac_mongodb_info')
    if _mongodb_info:
        _mongodb_name = _mongodb_info[-1].get('name')
        _tools_info = {
            'AssetVisibleName': [_mongodb_name]
        }
        Context.set('search_tools_name', _tools_info)

    SearchTools(
        name=data_scientist_searches_mongodb_in_marketplace.func_name
    ).run()


def data_scientist_searches_datasets_in_data_catalog():
    SearchDataSets(
        name=data_scientist_searches_datasets_in_data_catalog.func_name
    ).run()


def data_scientist_registers_template_using_DAC_CLI():
    RegisterTemplate(
        name=data_scientist_registers_template_using_DAC_CLI.func_name
    ).run()


def data_scientist_registers_asset_on_hadoop_using_DAC_CLI():
    RegisterAsset(
        name=data_scientist_registers_asset_using_DAC_CLI.func_name
    ).run()


def data_scientist_registers_asset_using_DAC_CLI():
    __to_register_assets = Context.get('to_register_assets')
    for register in __to_register_assets:
        register['hdfs_path'] = ''
    Context.set('to_register_assets',__to_register_assets)
    RegisterAsset(
        name=data_scientist_registers_asset_using_DAC_CLI.func_name
    ).run()


def data_scientist_submits_asset_using_DAC_CLI():
    SubmitAsset(
        name=data_scientist_submits_asset_using_DAC_CLI.func_name
    ).run()


def data_scientist_submits_template_using_DAC_CLI():
    SubmitTemplate(
        name=data_scientist_submits_template_using_DAC_CLI.func_name
    ).run()


def administrator_accepts_template_publication_using_DAC_CLI():
    AcceptTemplate(
        name=administrator_accepts_template_publication_using_DAC_CLI.func_name
    ).run()


def administrator_accepts_asset_publication_using_DAC_CLI():
    AcceptAsset(
        name=administrator_accepts_asset_publication_using_DAC_CLI.func_name
    ).run()


def administrator_rejects_template_publication_using_DAC_CLI():
    RejectTemplate(
        name=administrator_rejects_template_publication_using_DAC_CLI.func_name
    ).run()


def administrator_rejects_asset_publication_using_DAC_CLI():
    RejectAsset(
        name=administrator_rejects_asset_publication_using_DAC_CLI.func_name
    ).run()


def __main__():
    import os
    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _yaml_file = os.path.join(_parent_dir, 'config/config.yaml')

    # region WORKFLOW-TAF-361

    # _workflow_yaml_file = os.path.join(_parent_dir, 'config/E2EWF-5.config.yaml')
    # load_configurations(_yaml_file, _workflow_yaml_file)

    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_views_quota_information()
    # user_validates_permission()
    # administrator_adds_collaborators_to_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # data_scientist_accesses_workspace()
    # user_validates_permission()
    # data_scientist_deploys_services()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # data_scientist_accesses_workspace()
    # administrator_deletes_collaborators_within_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # data_scientist_accesses_workspace()
    # data_scientist_deploys_services()
    # data_scientist_logs_out_from_global_ui()

    # data_scientist_logs_in_to_global_ui()
    data_scientist_deletes_workspace()
    data_scientist_logs_out_from_global_ui()

    data_scientist_closes_browser()

    # endregion

    #region WORKFLOW-TAF-366

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-6.config.yaml')
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_retrieve_workbench_VM()
    # data_scientist_adds_asset_to_workbench_VM()
    # data_scientist_registers_asset_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_adds_tags_to_datasets()
    # # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_searches_mongodb_in_marketplace()
    # data_scientist_deploys_mongodb_dac_service()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_mongodb_dac()
    # data_scientist_deletes_deployed_workingsets()
    # data_scientist_deletes_deployed_tools()
    # # data_scientist_deletes_workspace()
    # #
    # data_scientist_logs_out_from_global_ui()

    # endregion

    # region WORKFLOW-TAF-368

    # _workflow_yaml_file = os.path.join(_parent_dir, 'config/E2EWF-7.config_int.yaml')
    # _workflow_yaml_file_1 = os.path.join(_parent_dir, 'config/E2EWF-0.config_int.yaml')
    # load_configurations(_yaml_file, _workflow_yaml_file, _workflow_yaml_file_1)
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_retrieve_workbench_VM()
    #
    # data_scientist_adds_asset_to_workbench_VM()
    # data_scientist_registers_asset_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_adds_tags_to_datasets()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_searches_cloudera_in_marketplace()
    # data_scientist_deploys_cloudera_clusters()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_cloudera()
    # data_scientist_deletes_deployed_tools()
    # data_scientist_deletes_workspace()

    #endregion

    #region WORKFLOW-TAF-369

    # _workflow_yaml_file = os.path.join(_parent_dir, 'config/E2EWF-8.config_int.yaml')
    # _workflow_yaml_file_1 = os.path.join(_parent_dir, 'config/E2EWF-0.config_int.yaml')
    # load_configurations(_yaml_file, _workflow_yaml_file, _workflow_yaml_file_1)
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_retrieve_workbench_VM()
    #
    # data_scientist_adds_asset_to_workbench_VM()
    # data_scientist_registers_asset_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_adds_tags_to_datasets()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_searches_hortonworks_in_marketplace()
    # data_scientist_deploys_hortonworks_clusters()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_hortonworks()
    # data_scientist_deletes_deployed_tools()
    # data_scientist_deletes_workspace()

    #endregion

    #region WORKFLOW-TAF-372

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config_int.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-10.config_int.yaml')
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_deploys_cloudera_clusters()
    # data_scientist_retrieve_workbench_VM()
    # data_scientist_adds_asset_to_cloudera_cluster()
    # data_scientist_registers_asset_on_hadoop_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_adds_tags_to_datasets()
    # data_scientist_deletes_registered_workingsets()
    # # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_deploys_mysql_pcf_service()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_mysql_pcf()
    # # data_scientist_deletes_workspace()
    # #
    # data_scientist_logs_out_from_global_ui()

    #endregion

    #region WORKFLOW-TAF-375

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-12.config.yaml')
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_deploys_cloudera_clusters()
    # data_scientist_retrieve_workbench_VM()
    # data_scientist_adds_asset_to_cloudera_cluster()
    # data_scientist_registers_asset_on_hadoop_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_deletes_registered_workingsets()
    # # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_adds_tags_to_datasets()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_workbench_vm()
    # # data_scientist_deletes_workspace()
    # #
    # data_scientist_logs_out_from_global_ui()

    #endregion

    #region WORKFLOW-TAF-376

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config_int.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-13.config_int.yaml')
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_deploys_cloudera_clusters()
    # data_scientist_adds_asset_to_cloudera_cluster()
    # data_scientist_registers_asset_on_hadoop_using_DAC_CLI()
    # data_scientist_publishes_tools()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_deletes_registered_tools()
    # # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_searches_tools_in_marketplace()
    # data_scientist_deploys_tools() # should be the default workbench VM
    # # data_scientist_deletes_workspace()
    #
    # data_scientist_logs_out_from_global_ui()

    #endregion

    #region WORKFLOW-TAF-378

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-15.config.yaml')
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_retrieve_workbench_VM()
    # data_scientist_adds_asset_to_workbench_VM()
    # data_scientist_registers_asset_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_adds_tags_to_datasets()
    # data_scientist_deletes_registered_workingsets()
    # # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_deploys_mysql_pcf_service()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_mysql_pcf()
    # data_scientist_deletes_deployed_workingsets()
    # data_scientist_deletes_deployed_pcf_instances()
    # # data_scientist_deletes_workspace()
    #
    # data_scientist_logs_out_from_global_ui()

    # endregion

    # region WORKFLOW-TAF-387

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-17.config.yaml')
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_retrieve_workbench_VM()
    # data_scientist_adds_asset_to_workbench_VM()
    # data_scientist_registers_asset_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_adds_tags_to_datasets()
    # data_scientist_deletes_registered_workingsets()
    # # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    # data_scientist_closes_browser()
    #
    # data_scientist_opens_browser()
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_searches_cloudera_in_marketplace()
    # data_scientist_deploys_cloudera_clusters()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_cloudera()
    # data_scientist_deletes_deployed_workingsets()
    # # data_scientist_deletes_workspace()
    # #
    # data_scientist_logs_out_from_global_ui()

    # endregion

    #region WORKFLOW-TAF-388

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config_int.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-18.config_int.yaml')
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_retrieve_workbench_VM()
    # data_scientist_adds_asset_to_workbench_VM()
    # data_scientist_registers_asset_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_adds_tags_to_datasets()
    # # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_searches_cloudera_in_marketplace()
    # data_scientist_deploys_cloudera_clusters()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_cloudera()
    # # data_scientist_deletes_workspace()
    # #
    # data_scientist_logs_out_from_global_ui()

    #endregion

    #region WORKFLOW-TAF-389

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config_int.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-21.config_int.yaml'),
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_retrieve_workbench_VM()
    # data_scientist_adds_asset_to_workbench_VM()
    # data_scientist_registers_asset_using_DAC_CLI()
    # data_scientist_publishes_tools()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_deletes_registered_tools()
    # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_searches_tools_in_marketplace()
    # data_scientist_deploys_tools()
    # data_scientist_deletes_deployed_tools()
    # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_closes_browser()

    #endregion

    #region WORKFLOW-TAF-390

    # _workflow_yaml_file = [
    #     os.path.join(_parent_dir, 'config/E2EWF-0.config_int.yaml'),
    #     os.path.join(_parent_dir, 'config/E2EWF-20.config_int.yaml')
    # ]
    # load_configurations(_yaml_file, *_workflow_yaml_file)
    #
    # data_scientist_opens_browser()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_retrieve_workbench_VM()
    # data_scientist_adds_asset_to_workbench_VM()
    # data_scientist_registers_asset_using_DAC_CLI()
    # data_scientist_publishes_datasets()
    # administrator_accepts_asset_publication_using_DAC_CLI()
    # data_scientist_adds_tags_to_datasets()
    # data_scientist_deletes_registered_workingsets()
    # # data_scientist_deletes_workspace()
    # data_scientist_logs_out_from_global_ui()
    #
    # data_scientist_logs_in_to_global_ui()
    # # data_scientist_creates_workspace()
    # data_scientist_accesses_workspace()
    # data_scientist_searches_datasets_in_data_catalog()
    # data_scientist_deploys_datasets_to_workbench_vm()
    # data_scientist_deletes_deployed_workingsets()
    # # data_scientist_deletes_workspace()
    # #
    # data_scientist_logs_out_from_global_ui()

    #endregion

main = __main__

if __name__ == "__main__":
    __main__()
