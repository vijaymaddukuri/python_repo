# Ozone Framework

This repository contains all the source code used for Ozone Framework and build instructions.

The code is divided into the following sections:

 - web - Contains the source code for the Web Framework
 - ozone-scripts - Contains the source code for Supporting Python Modules and Ansible Playbooks

## Build
The Ozone framework along with the web server and supporting scripts can be built using Docker.
Clone this repository into a Linux system with Docker installed and run the below command to build:

 > Note: You must have the VMware OVFTool downloaded to the same directory beside the docker file.
 > The OVFTool can be downloaded from [here](https://my.vmware.com/group/vmware/details?downloadGroup=OVFTOOL410&productId=491).
 > Choose the 64 bit Linux version.
 > File name must be VMware-ovftool-4.1.0-2459827-lin.x86_64.bundle. If different edit it in the Dockerfile

 ```
 docker build -t ozone .
 ```

## Run

Run using `docker run`. A data volume is required to persist database data. Create a local mount 
(directory if sufficient free space is available in the default filesystem)  and provide that as an argument
 for the docker run command with the option `-v <host directory>:/data`

```
 docker run -v /data:/data ozone
 ```

### Author
Mumshad Mannambeth - <mumshad.mannambeth@dell.com>


