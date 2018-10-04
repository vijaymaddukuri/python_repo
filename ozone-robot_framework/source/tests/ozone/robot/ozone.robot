*** Settings ***
Library     ozone.workflow.BaseWorkflow
Documentation       Demo  Workflow
Suite Setup     Initiate Suite

*** Test Cases ***
Ozone workflow
##    Deploy Ozone vAPP
##    sleep  3m
#    Start Ozone Session
##    Configure Ozone vAPP
##    Create Project
#    Update Project Variables
##    Execute Prevalidation Playbook
#    Execute Main Playbook
##    Delete Project
    Log     Test ci run

*** Keywords ***
Initiate Suite
    Apply Settings From Files       C:/ozone_dev/ozone/source/tests/ozone/config/generic.yaml      C:/ozone_dev/ozone/source/tests/ozone/config/workflow_vpod2.yaml
    Start Vcenter Session