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


/**
 * Populate DB with sample data on server start
 * to disable, edit config/environment/index.js, and set `seedDB: false`
 */

'use strict';
import appconfig from './environment';
var couchStore = require('../components/dbConnect/couchdbConnect');

import User from '../api/user/user.model';

//User.find({}).remove()
//  .then(() => {
    /*User.create(/!*{
      provider: 'local',
      name: 'Test User',
      email: 'test@ozone.com',
      password: 'ozone'
    }, {
      provider: 'local',
      role: 'admin',
      name: 'Admin',
      email: 'admin@ozone.com',
      password: 'ozone'
    },*!/ {
      provider: 'local',
      role: 'admin',
      name: 'AnsibleOzoneConnect2',
      email: 'ansibleozoneconnect@ozone.com',
      password: 'ansibleConnect'
    })
    .then(() => {
      console.log('finished populating users');
    });*/
//  });



var createUserIfNotExists = function(username, email, role, provider, password){

  User.findone({name:username}).then(user => {
    if(!user.length){
    console.log('Local user does not exist. Creating - ' + username);
    User.create(
      {
        provider: provider,
        role: role,
        name: username,
        email: email,
        password: password
      })
      .then(() => {
      console.log('Created ' + username + ' User');
  });
  }else{
    console.log('Local user already exists - ' + username);
  }
});
};


console.log("Establishing database connection");
couchStore.createCouchDB(appconfig.couch.server,
  appconfig.couch.port,
  appconfig.couch.database,
  appconfig.couch.userName,
  appconfig.couch.password, function(response){
    console.log("Database Connectivity established")
  }, function(error){
    console.log("Error creating database " + error)
  });

console.log('waiting for DB creation');
// TODO: Improve
setTimeout(function() {
  console.log('Creating default users');
  createUserIfNotExists('Admin','admin@ozone.com','admin','local', 'ozone');
  createUserIfNotExists('AnsibleOzone','ansibleozoneconnect@ozone.com','admin','local', 'ansibleConnect');
  createUserIfNotExists('ehc','ehc@ozone.com','user','local', 'ehc');
  createUserIfNotExists('superadmin','superadmin@ozone.com','superadmin','local', 'Ozone123!');
  createUserIfNotExists('service','service@ozone.com','service','local', 'Ozone123!');

}, 10000);



