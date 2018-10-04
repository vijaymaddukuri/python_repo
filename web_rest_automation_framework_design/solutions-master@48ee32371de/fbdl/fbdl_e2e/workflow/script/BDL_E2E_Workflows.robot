*** Settings ***
Library           /usr/lib/python2.7/site-packages/fbdl_e2e/keywords/

*** Test Cases ***
[E2EWF-0] Data scientist can ingest a customized template and asset
    [Documentation]    As a data scientist,I want to ingest a customized template, so that I can ingest my assets with it.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Data Scientist Logs In To Global Ui
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Comment    Data Scientist Add templates to workbench
    Data Scientist Adds Asset To Workbench VM
    Comment    Data Scientist Add asset to workbench
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Template Using DAC CLI
    Data Scientist Submits Template Using DAC CLI
    Administrator Accepts Template Publication Using DAC CLI
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Submits Asset Using DAC CLI
    Administrator Rejects Asset Publication Using DAC CLI
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Submits Asset Using DAC CLI
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-2]Data scientist can deploy data set to PCF MySQL
    [Documentation]    As a data scientist, I want to deploy data set to a MySQL data container, so that I can do data analysis with this data set.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-2.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Deploys Mysql Pcf Service
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets to Mysql Pcf
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-3]Data scientist can deploy data set to workbench VM
    [Documentation]    As a data scientist, I want to deploy dataset to workbench VM
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-3.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets to Workbench VM
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-4]Data scientist can deploy rpm installer to workbench VM
    [Documentation]    As a data scientist, I want to deploy rpm installer to workbench VM, so that I can use this tool to do data analysis.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-4.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Tools
    Administrator Accepts Asset Publication Using DAC CLI
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Tools In Marketplace
    Data Scientist Deploys Tools
    Data Scientist Deletes Deployed Tools
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-5]Data scientist creates new workspace and manage access permission
    [Documentation]    As a data scientist, I want to create workspace and grant access permissions, so that workspace members can work together.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-5.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Views Quota Information
    User Validates Permission
    Administrator Adds Collaborators To Workspace
    Data Scientist Logs Out From Global Ui
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Data Scientist Accesses Workspace
    User Validates Permission
    Data Scientist Deploys Services
    Data Scientist Logs Out From Global Ui
    Comment    Data Scientist A Logs In to Global UI Again
    Data Scientist Logs In To Global Ui
    Data Scientist Accesses Workspace
    Administrator Deletes Collaborators Within Workspace
    Data Scientist Logs Out From Global Ui
    Comment    Data Scientist B Logs In to Global UI Again
    Data Scientist Logs In To Global Ui
    Data Scientist Accesses Workspace
    Data Scientist Deploys Services
    Data Scientist Logs Out From Global Ui
    Comment    Data Scientist A Logs In to Global UI to delete workspace
    Data Scientist Logs In To Global Ui
    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-6]Data scientist can deploy dataset to MongoDB
    [Documentation]    As a data scientist, I want to deploy dataset to MongoDB, so that I can work with it.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-6.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Data Scientist Deletes Registered Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Mongodb In Marketplace
    Data Scientist Deploys Mongodb Dac Service
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Mongodb Dac
    Data Scientist Deletes Deployed Workingsets
    Data Scientist Deletes Deployed Tools
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-7]Data scientist can deploy data set to Cloudera
    [Documentation]    As a data scientist, I want to deploy data set into Cloudera cluster, so that I can do data analysis with this data set.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-7.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment   Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset to Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment   Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Cloudera in Marketplace
    Data Scientist Deploys Cloudera Clusters
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Cloudera
    Comment   Data Scientist Deletes Deployed Tools
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-8]Data scientist can deploy data set to Hortonworks
    [Documentation]    As a data scientist, I want to deploy data set into Hortonworks cluster, so that I can do data analysis with this data set.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-8.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment   Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset to Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment   Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Hortonworks in Marketplace
    Data Scientist Deploys Hortonworks Clusters
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Hortonworks
    Comment   Data Scientist Deletes Deployed Tools
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-10]Data scientist can deploy data set reside on hadoop to PCF MySQL
    [Documentation]    As a data scientist, I want to deploy data set which resides on hadoop to a MySQL data container, so that I can do data analysis with this data set.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-10.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Deploys Cloudera Clusters
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Cloudera Cluster
    Data Scientist Registers Asset On Hadoop Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Data Scientist Deletes Registered Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Deploys Mysql Pcf Service
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Mysql Pcf
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-11]Data scientist can deploy directory to workbench VM
    [Documentation]    As a Data scientist, I want to deploy directory to workbench VM and share to other data scientists
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-11.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Submits Asset Using DAC CLI
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets to Workbench VM
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-12]Data scientist can deploy directory reside on Hadoop to workbench VM
    [Documentation]    As a data scientist, I want to deploy directory reside on Hadoop, so that I can work with it.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-12.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Comment    Data Scientist A Deploys Hadoop Clusters
    Data Scientist Deploys Cloudera Clusters
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Cloudera Cluster
    Data Scientist Registers Asset On Hadoop Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Deletes Registered Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Tags To Datasets
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Workbench Vm
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-13]Data scientist can deploy rpm installer reside on Hadoop to workbench VM
    [Documentation]    As a data scientist, I want to deploy rpm installer reside on Hadoop, so that I can work with it.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-13.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Comment    Data Scientist A Deploys Hadoop Clusters
    Data Scientist Deploys Cloudera Clusters
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Cloudera Cluster
    Data Scientist Registers Asset On Hadoop Using DAC CLI
    Data Scientist Publishes Tools
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Deletes Registered Tools
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Tools In Marketplace
    Data Scientist Deploys Tools
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-14]Data scientist can remove workingset deployed to workbench VM
    [Documentation]    As a data scientist, I want to remove the deployed workingset from workbench VM, so that I can save resources.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-14.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Data Scientist Deletes Registered Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets to Workbench VM
    Data Scientist Deletes Deployed Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-15]Data scientist can remove workingset deployed to PCF MySQL
    [Documentation]    As a data scientist, I want to remove the deployed workingset from PCF MYSQL, so that I can save resources.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-15.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Data Scientist Deletes Registered Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Deploys Mysql Pcf Service
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets to Mysql Pcf
    Data Scientist Deletes Deployed Workingsets
    Data Scientist Deletes Deployed Pcf Instances
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-17]Data scientist can remove data set deployed to Hadoop (Cloudera)
    [Documentation]    As a data scientist, I want to remove dataset deployed to Hadoop, so that I can save some resources.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-17.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Data Scientist Deletes Registered Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Cloudera In Marketplace
    Data Scientist Deploys Cloudera Clusters
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Cloudera
    Data Scientist Deletes Deployed Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-18]Data scientist can deploy directory to Hadoop (Cloudera)
    [Documentation]    As a data scientist, I want to deploy directory to Hadoop, so that I can work with it.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-18.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Cloudera In Marketplace
    Data Scientist Deploys Cloudera Clusters
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Cloudera
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-19]Data scientist can remove directory deployed to Hadoop (Cloudera)
    [Documentation]    As a data scientist, I want to remove directory deployed to Hadoop.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-19.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Data Scientist Deletes Registered Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Cloudera in Marketplace
    Data Scientist Deploys Cloudera Clusters
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Cloudera
    Data Scientist Deletes Deployed Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-20]Data scientist can remove directory deployed to workbench VM
    [Documentation]    As a data scientist, I want to remove directory deployed to workbench VM, so that I can save some resources.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-20.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Datasets
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Adds Tags To Datasets
    Data Scientist Deletes Registered Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Datasets In Data Catalog
    Data Scientist Deploys Datasets To Workbench VM
    Data Scientist Deletes Deployed Workingsets
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser

[E2EWF-21]Data scientist can remove deployed tool from workbench VM
    [Documentation]    As a data scientist, I want to remove the deployed tool, so that I can save resources.
    [Tags]    E2E WORKFLOW
    [Setup]    Load Configurations    /root/automation/bdl/config/config.yaml    /root/automation/bdl/config/E2EWF-0.config.yaml    /root/automation/bdl/config/E2EWF-21.config.yaml
    [Teardown]    Clean Up Environment
    Data Scientist Opens Browser
    Comment    Data Scientist A Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Adds Asset To Workbench VM
    Data Scientist Registers Asset Using DAC CLI
    Data Scientist Publishes Tools
    Administrator Accepts Asset Publication Using DAC CLI
    Data Scientist Deletes Registered Tools
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
    Data Scientist Opens Browser
    Comment    Data Scientist B Logs In to Global UI
    Data Scientist Logs In To Global Ui
    Comment    Data Scientist Creates Workspace
    Data Scientist Accesses Workspace
    Data Scientist Retrieve Workbench VM
    Data Scientist Searches Tools In Marketplace
    Data Scientist Deploys Tools
    Data Scientist Deletes Deployed Tools
    Comment    Data Scientist Deletes Workspace
    Data Scientist Logs Out From Global Ui
    Data Scientist Closes Browser
