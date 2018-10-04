#
# Copyright (c) 2016 DELL EMC Corporation
# All Rights Reserved
#
# This software contains the intellectual property of DELL EMC Corporation
# or is licensed to DELL EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of DELL  EMC.
#

# Pull base image.
FROM emccorp/docker-node-couch-redis-ansible

MAINTAINER Mumshad Mannambeth <mumshad.mannambeth@dell.com>

# ----------------------------------------------------------------
# Configure dependencies
# ----------------------------------------------------------------

# Install Dependencies
RUN zypper update -y && zypper install -y rsync vim python3-pip iputils net-tools


# Reset root password - this will be used by Web server to access local system
RUN echo "root:P@ssw0rd@123" | chpasswd

# Setup Ansible Vault Password
RUN echo "P@ssw0rd@123"  > /root/.vault_pass.txt

#Install openssh and Enable PermitRootLogin in sshd config file and restart sshd_server
RUN zypper install -y openssh && ssh-keygen -A && \
    sed -i "s/#UsePrivilegeSeparation.*/UsePrivilegeSeparation no/g" /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

# Copy python script dependencies
RUN mkdir -p /opt/ozone-scripts/ehc-python-scripts
#COPY ozone-scripts/ehc-python-scripts/dependecies /opt/ozone-scripts/ehc-python-scripts/dependecies

# Install python scripts depndencies

#&& pip2 install -r /opt/ozone-scripts/ehc-python-scripts/dependecies

# Upgrade Ansible
RUN zypper install -y libressl-devel
RUN pip2 install --upgrade pip

#commented this on 1/2/2017
#RUN zypper install -y python3-devel openssl libopenssl-devel && pip2 install ansible --upgrade


# Install Python3 Dependencies for Python Scripts for Python3.5 for Supporting Scripts
RUN pip install pd && pip install pydevd && pip install pysphere && pip install pyVmomi && pip install "pywinrm>=0.1.1"

# Install Python Modules for Python2.7 for Ansible
RUN pip2 install pd && pip2 install pydevd && pip2 install pysphere && pip2 install pyVmomi && pip2 install "pywinrm>=0.1.1" && pip2 install redis && pip2 install netaddr && pip2 install filelock && pip2 install jmespath


# M2Crypto installed with pip in Ubuntu has issues https://github.com/saltstack/salt/issues/391
# Install lighttpd

RUN zypper update -y && zypper install -y lighttpd
COPY config/lighttpd.conf /etc/lighttpd/lighttpd.conf
COPY config/server.pem /etc/lighttpd/server.pem

EXPOSE 443
EXPOSE 80

# ----------------------------------------------------------------
# Install Node Kue
# ----------------------------------------------------------------
RUN mkdir -p /opt/kue
WORKDIR /opt/kue

RUN npm install kue

# Increase json body parser limit to support larger data. This is for Kue to add large data to logs.
RUN sed -i "s/bodyParser.json()/bodyParser.json({limit:'50mb'})/" /opt/kue/node_modules/kue/lib/http/index.js

EXPOSE 3000

# ----------------------------------------------------------------
# Bundle Web Application
# ----------------------------------------------------------------

# Create app directory
RUN mkdir -p /opt/web/logs
WORKDIR /opt/web

# Install app dependencies
COPY web/package.json /opt/web
RUN npm install phantomjs-prebuilt
RUN npm install

# Install bower dependencies
COPY web/bower.json /opt/web
COPY web/.bowerrc /opt/web
RUN bower install --allow-root

# Install correct version of Ansible. Move this further up in the future to reduce build time.
RUN pip2 install ansible==2.2.1.0

# COPY Lighttpd Dependencies. Move this further up in the future to reduce build time.
RUN mkdir -p /usr/share/lighttpd/
COPY dependency/lighttpd/* /usr/share/lighttpd/
RUN chmod 777 /usr/share/lighttpd/*

COPY web /opt/web
COPY web/grunt-script.sh /opt/web

ENV PORT=9000 NODE_ENV=development
EXPOSE 9000

# Build Web Application
RUN grunt serve:prod

# ----------------------------------------------------------------
# Copy Service Configuration Files and Docker Startup Script
# ----------------------------------------------------------------
# Copy Service Configuration Files
COPY config/* /etc/

# ----------------------------------------------------------------
# Copy Supporting Ozone Scripts -Python Modules and Ansible Playbooks
# ----------------------------------------------------------------
COPY ozone-scripts /opt/ozone-scripts

# Temporary workaround to get Python3.4 working with Python3.5
#RUN cp /usr/bin/python3.5 /usr/bin/python3.4

# Copy docker startup script
COPY docker-startup-script.sh /opt/
RUN chmod 755 /opt/docker-startup-script.sh && chmod 755 /opt/ozone-scripts/scripts/vault-pass-script.sh
RUN chmod a-x /opt/ozone-scripts/scripts/vault-pass-script.sh

# Configure docker ENTRYPOINT
ENTRYPOINT /opt/docker-startup-script.sh

# Copy couchDB Configuration File
COPY config/couchdb.ini /etc/couchdb/default.ini

