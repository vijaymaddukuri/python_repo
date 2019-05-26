#TODO update README for better readability
########## Backup Automation ##########

########### Backup Service Test Automation ##########

What to install?

pip2.7 install pyyaml

pip2.7 install requests

pip2.7 install robotframework

pip2.7 install robotframework-requests

pip2.7 install robotframework-httplibrary

pip2.7 install simple-yaml

pip2.7 install selenium

pip2.7 install robotframework-selenium2library

pip2.7 install paramiko

export PYTHONPATH=$PYTHONPATH:$dir/TAveche


########## How to run? ##########
For sanity
robot -b debuglogs.txt -L DEBUG:INFO -d logs -x junit.xml --timestampoutputs validate.robot

For full automation
robot -b debuglogs.txt -L DEBUG:INFO -d logs -x junit.xml --timestampoutputs backup_automation.robot

########## How to check results ? ##########

Results are available in the logs folder in the below location

$dir\TAveche\robot_tests\backup_service_automation\logs



