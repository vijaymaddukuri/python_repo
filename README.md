This project contains following projects:

Pyvmomi scripts:

    Deploy OVA
    power cycles of VM
    Export OVA

Django App:

    To create sample web url using django

Robot Framework designs:
    Web and REST, automation framewework designs
    Ozone robot framework

SSH project:

    SSH utility using paramiko library to execute commands in remote machine, upload files to remote machine

POC on Salt cloud:

    Designing of cloud driver using Salt stack (Salt cloud)

CI/CD:

    Jenkins pipeline with groovy scripting for end to end automation.

Devops:

    Sample dockerfile for CI/CD
Common:

   Dict to yaml conversion, getting value from yaml file and unit test cases.


Training:
    Code wars, hackerrank solved python scripts.


### Software Requirments

    Python 3.5 or 2.7


### Python Virtual Environment

1. Create Python virtual environment
    
        $ virtualenv mw_venv -p python3
    
2. Activate virtual environment 
    
        $ source mw_venv/bin/activate
    
3. Deactivate virtual environment
    
        $ deactivate
    

### Install requirements

* Install python project dependencies for dev environment
   
        $ pip3 install -r requirements/local.txt

    

### Run Flake8 before commit (run on the root of the project)

        $ flake8