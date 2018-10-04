*** Settings ***
Documentation          This test suite test Ansible Playbook for Input Validation


Library                SSHLibrary
Suite Setup            Open Connection And Log In
Suite Teardown         Close All Connections
Test Template          Execute Ansible Playbook And Verify Output
Resource               resource.robot


*** Variables ***
${HOST}                     localhost
${PORT}                     9322
${USERNAME}                 root
${PASSWORD}                 P@ssw0rd@123
${ANSIBLE_VAULT_PASSWORD}   P@ssw0rd@123
${ANSIBLE_PROJECT_DIR}      /data/ehc-builder-projects/Project1_0901050948
${ANSIBLE_PLAYBOOK}         Master-EHC-41-Deploy-and-Configure.yml
${ANSIBLE_INVENTORY_FILE}   inventory
${ANSIBLE_VAULT_PASSWORD_FILE}  /opt/ozone-scripts/scripts/vault-pass-script.sh

*** Test Cases ***                 TAG                                                    EXPECTED RETURN CODE          EXTRA VARS
Invalid Hostname                PRV-01 - Validate Input data for Virtual Machines       ${ANSIBLE_RC_HOST_FAILED}      '{"host_address": {"vra_web_secondary": {"ip": "10.247.", "fqdn": "lglas209.ehcdomain2.local"}}}'
Valid Hostname                  PRV-01 - Validate Input data for Virtual Machines       ${ANSIBLE_RC_OK}               ''


*** Keywords ***
Open Connection And Log In
   Open Connection    ${HOST}  port=${PORT}  term_type=ansi
   Login    ${USERNAME}    ${PASSWORD}

Execute Ansible Playbook
    [Arguments]    ${tag}   ${extra_vars}
    @{rc}=  Execute Command    export ANSIBLE_HASH_BEHAVIOUR=merge; export ANSIBLE_HOST_KEY_CHECKING=False; export ANSIBLE_CALLBACK_PLUGINS=callback_plugins; export ANSIBLE_VAULT_PASSWORD=${ANSIBLE_VAULT_PASSWORD}; cd "${ANSIBLE_PROJECT_DIR}"; ansible-playbook "${ANSIBLE_PLAYBOOK}" -i "${ANSIBLE_INVENTORY_FILE}" --vault-password-file ${ANSIBLE_VAULT_PASSWORD_FILE} --tags "${tag}" -v --extra-vars ${extra_vars}       return_rc=True
    Log     @{rc}[1]
    [Return]  @{rc}

Execute Ansible Playbook And Verify Output
    [Documentation]    Execute Ansible playbook and verify output
    [Arguments]    ${tag}  ${expected_rc}   ${extra_vars}
    @{rc}=  Execute Ansible Playbook    ${tag}  ${extra_vars}
    #${rc}=    Execute Command    hostname
    Should Be Equal    @{rc}[1]    ${expected_rc}