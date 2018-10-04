#! /bin/bash

#
# Script to get Ansible Vault Password. Password may be set in the process's environment variable during Playbook execution
# This script could be modified to fetch password from else where to increase security
#

echo "$ANSIBLE_VAULT_PASSWORD"
