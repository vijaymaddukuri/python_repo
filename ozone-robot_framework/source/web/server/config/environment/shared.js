/*
 * Copyright (c) 2016 DELL EMC Corporation
 * All Rights Reserved
 *
 * This software contains the intellectual property of DELL EMC Corporation
 * or is licensed to DELL EMC Corporation from third parties.  Use of this
 * software and the intellectual property contained therein is expressly
 * limited to the terms and conditions of the License Agreement under which
 * it is provided by or on behalf of DELL  EMC.
 */


'use strict';

module.exports = {
  // List of user roles
  ozoneVersion: '0.4.8',
  userRoles: ['guest', 'user', 'monitor','deploy','configure', 'admin', 'superadmin','service'],
  'defaults':{
    'EHC4.1.1':{},
    'EHC4.5.0':{}
  },
  'scriptEngine' : {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'P@ssw0rd@123',
    'inputDirectory': '/opt/ozone-scripts/ehc-python-modules/input',
    'url_check_script': '/opt/ozone-scripts/ehc-python-modules/bin/url_check.sh',
    'configure' : 'python3.4 /opt/ozone-scripts/ehc-python-modules/bin/configure.py',
    'snapshot' : 'python3.4 /opt/ozone-scripts/ehc-python-modules/bin/Snapshot.py',
    'monitor' : 'python3.4 /opt/ozone-scripts/ehc-python-modules/bin/monitor.py',
    'deployVMFromOvfTemplate' : 'python3.4 /opt/ozone-scripts/ehc-python-modules/bin/Deploy_VM_from_Template.py',
    'projectsFolder' : '/data/ehc-builder-projects/',
    'ansibleProjectTemplates': '/opt/ozone-scripts/ehc-ansible-project-templates/'
  },
  redis: {
    host: 'localhost',
    port  : 6379  , // Port of your locally running Redis server
    scope : 'kue',  // Scope of NRPs messaging
  },
  kue:{
    host: 'localhost',
    port: '3000'
  }
};
