### EHC Ansible Roles

This is a project built to support EMC Enterprise Hybrid Cloud deployment automation. This project is a part of the [Ozone](https://ozone.lss.emc.com) tool being built to automate deployment and initial configurations of EMC Enterprise Hybrid Cloud.

This project focuses on the development of Ansible roles which will be integrated to the backend of [Ozone](https://ozone.lss.emc.com).

Checkout [Wiki](http://lglas071.lss.emc.com/ehc/ehc-ansible-roles/wikis/home) page for more documentation.

### Knowledge Requirement

If you are not familiar with these technologies, get started here:
* [git](https://git-scm.com/) - For sharing and collaborating work between team members. An interactive course is available at [CodeSchool](https://www.codeschool.com/courses/try-git). You should be set in an hour.
* [Ansible](https://www.ansible.com/) - Automation and Orchestration Engine that is the backbone of Ozone. Start learning [here](http://docs.ansible.com/ansible/intro.html)
* EMC Enterprise Hybrid Cloud - You know how to get started on this. ;-)

### Getting Started

Clone this repository following instructions below. 

Install `git` on your development Linux system. 
Ansible development system must be linux as Ansible controller is only supported on a Linux Machine. 

Change to development directory and clone this repository: Use your EMC NTID and password to clone.

```console
git clone http://lglas071.lss.emc.com/ehc/ehc-ansible-roles.git
Cloning into 'ehc-ansible-roles'...
Username for 'http://lglas071.lss.emc.com': mannam4
Password for 'http://mannam4@lglas071.lss.emc.com':
remote: Counting objects: 57, done.
remote: Compressing objects: 100% (39/39), done.
remote: Total 57 (delta 3), reused 0 (delta 0)
Unpacking objects: 100% (57/57), done.
Checking connectivity... done.
```

`cd` to the folder `ehc-ansible-roles`

### Ansible Project Structure

This Ansible project is strctured as per Ansible best practices found [here](http://docs.ansible.com/ansible/playbooks_best_practices.html)

```YAML
production                # inventory file for production servers
staging                   # inventory file for staging environment

group_vars/
   group1                 # here we assign variables to particular groups
   group2                 # ""
host_vars/
   hostname1              # if systems need specific variables, put them here
   hostname2              # ""

library/                  # if any custom modules, put them here (optional)
filter_plugins/           # if any custom filter plugins, put them here (optional)

site.yml                  # master playbook
webservers.yml            # playbook for webserver tier
dbservers.yml             # playbook for dbserver tier

roles/
    common/               # this hierarchy represents a "role"
        tasks/            #
            main.yml      #  <-- tasks file can include smaller files if warranted
        handlers/         #
            main.yml      #  <-- handlers file
        templates/        #  <-- files for use with the template resource
            ntp.conf.j2   #  <------- templates end in .j2
        files/            #
            bar.txt       #  <-- files for use with the copy resource
            foo.sh        #  <-- script files for use with the script resource
        vars/             #
            main.yml      #  <-- variables associated with this role
        defaults/         #
            main.yml      #  <-- default lower priority variables for this role
        meta/             #
            main.yml      #  <-- role dependencies

    ansible-role-deploy-ovfs/           # Deploy all EHC OVF Components
    ansible-role-deploy-windows/        # Deploy EHC Windows Systems from tempate and configure network.
    ansible-role-prepare-vcenter/       # Prepare vCenter tasks such as copying ISO images to datastore
    ansible-role-vra/                   # Deploy and Configure vRA Automation
```

What we will be focusing now are the [ansible roles](http://docs.ansible.com/ansible/playbooks_roles.html). I have been working on developing ansible roles to deploy all required OVFs and some windows systems form template.
Our primary task is to build out ansible-roles for individual modules.

#### Environment Details

All environment information are stored in common role - `ehc-ansible-roles/roles/common/vars/main.yml`

```YAML
---
# vars file for common

#Common Network Information
network_gateway: 10.123.134.1
network_mask: 255.255.255.0
network_dns_servers: 10.123.134.237, 10.123.134.237
network_dns_server1: 10.123.134.237
network_dns_server2: 10.123.134.237

# vsphere information
vcenter_hostname: 10.123.135.25
vcenter_port: 443
vcenter_username: administrator@vsphere.local
vcenter_password: VMwar3!!
vcenter_datacenter: Datacenter1

esxi_datacenter: Datacenter1
esxi_hostname: host1.ehc.local
esxi_cluster: Auto

windows_server_template: 'Windows Server 2012 Template'
sql_iso_datastore_path: DS_share/images/SQLFULL_ENU.iso


sql_server_hostname: net084.lss.emc.com
sql_server_ip: 10.123.69.84
sql_server_username: administrator
sql_server_password: P@ssw0rd@123

```

Update this file with your enviromental details.

#### Executing/Testing a role

In order to execute an ansible-role say - 'deploy-all-ovfs' , run the ansible playbook in the test folder.

* `cd` to roles folder
    ```
    cd ehc-ansible-roles/roles/
    ```
* Run the playbook with ansible playbook command
    ```
    ansible-playbook "ansible-role-deploy-ovfs/tests/test.yml" -i "ansible-role-deploy-ovfs/tests/inventory"
    ```
    Note: For ovf-deploy to work you need [OVFtool 4.1](https://my.vmware.com/web/vmware/details?productId=491&downloadGroup=OVFTOOL410) installed.

Note: You are exepcted to run across issues the first time. I have only tested in my environment. We need to make it work in all environments. So feel free to standardize push back changes. Reach out to me for help any time.


### How can you help?
I need all the help I can get, starting with:
- Building ansible-roles for automating each component
- Building ansible modules if anything is not supported out of the box
- Testing and reporting bugs - use Issue tracker [here](http://lglas071.lss.emc.com/ehc/ehc-ansible-roles/issues)
- Planning - Use Issue tracker [here](http://lglas071.lss.emc.com/ehc/ehc-ansible-roles/issues) to create feature requests and label them accrodingly.
- Project Management
- Maintaing this repository
- Documentation - Document everything in the [wiki](http://lglas071.lss.emc.com/ehc/ehc-ansible-roles/wikis/home)
- vAPP building - I am building a vAPP with pre installed Ozone and ansible project. Its a different project, but I could use some help. Check it out [here](http://lglas071.lss.emc.com/root/ozone-vapp)
- Web development for Ozone (Phase 2 - and done on a different project [here](http://lglas071.lss.emc.com/ehc/ozone))

### Contribution Guide

Check out [contribution guide](http://lglas071.lss.emc.com/ehc/ehc-ansible-roles/blob/master/CONTRIBUTING.md) on how to build your modules and contribute 

### Reference

There are a lot of Ansible-Roles built for these purposes already. Some interesting ones are listed below:
[ansible-role-vcenter](https://github.com/vmware/ansible-role-vcenter)
[ansible-role-vra](https://github.com/vmware/ansible-role-vra)
[ansible-role-vrops](https://github.com/vmware/ansible-role-vrops)
[ansible-role-vrb](https://github.com/vmware/ansible-role-vrb)
[ansible-role-nsx](https://github.com/vmware/ansible-role-nsx)

More from VMWare [here](https://github.com/vmware?utf8=%E2%9C%93&query=ansible-role)

### Some Extra Configurations
The default ansible module vmware_vm_shell does not work with self-signed certificates. Add the below lines to the file
/usr/lib/python2.7/site-packages/ansible/modules/extras/cloud/vmware/vmware_vm_shell.py
```
try:
    from pyVmomi import vim, vmodl
    HAS_PYVMOMI = True
except ImportError:
    HAS_PYVMOMI = False

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/execute_program_in_vm.py
def execute_command(content, vm, vm_username, vm_password, program_path, args="", env=None, cwd=None):

```


## Contact
Mumshad Mannambeth - Mumshad.Mannambeth@emc.com