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

// Production specific configuration
// =================================
module.exports = {
  mongo: {
    uri: process.env.MONGO_URI || 'mongodb://localhost:27017/ehcbuilder-dev'
    // uri: process.env.MONGO_URI || 'mongodb://localhost:27017/ehcbuilder-dev'
  },
  'ldap':{
    url: 'ldap://emcroot.emc.com:3268',
    domain: 'corp'
  },
  'email' : {
    'disabled': false,
    'smtpServer' : 'mailhub.lss.emc.com',
    'smtpServerPort' : '25',
    'email_admins' : 'mumshad.mannambeth@emc.com',
    'from_email': 'ehc_builder@emc.com'
  }
};
