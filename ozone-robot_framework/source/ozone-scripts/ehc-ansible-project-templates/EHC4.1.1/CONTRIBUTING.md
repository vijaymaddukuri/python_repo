### Getting Started

If you are not familiar with these technologies, get started here:
* [git](https://git-scm.com/) - For sharing and collaborating work between team members. An interactive course is available at [CodeSchool](https://www.codeschool.com/courses/try-git). You should be set in an hour.
* [Ansible](https://www.ansible.com/) - Automation and Orchestration Engine that is the backbone of Ozone. Start learning [here](http://docs.ansible.com/ansible/intro.html)
* EMC Enterprise Hybrid Cloud - You know how to get started on this. ;-)

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

### Contribution Guide

Checkout [Issues](http://lglas071.lss.emc.com/ehc/ehc-ansible-roles/issues) page for outstanding work. Pick a feature case and assign to self. 
If one does not exist (which is probably the case now), feel free to create it and label it feature.
Develop the Ansible Roles and push it back to the repository following instructions below.

CD into the cloned directory if you haven't already done so:
```
cd ehc-ansible-roles
```

Create a new local git branch in your system for the feature you are developing. Use format feature-<issue number>-<feature-name>. eg 'feature-3-vipr':
```
git branch feature-3-vipr
```

Checkout the new branch:
```
git checkout feature-3-vipr
```

Make your changes. Once done, commit your changes and push to remote.

```
git commit -am "Added new feature for vipr"
git push --set-upstream origin feature-vipr
```

Your changes will now be in the remote repository, but still on a difference branch. (Not part of the master code)
To merge your changes to the master code:
- Login to the git repository - http://lglas071.lss.emc.com/ehc/ehc-ansible-roles
- Select your new branch from the drop down
- Click on Create Merge Request

A new merge request will be created, reviewed, approved and changes will be part of the master code.
