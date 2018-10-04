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

/**
 * @module
 * @name kueTaskStatusProcessor
 * @description Kue Task Status Processor to update job status by Ansible.
 * Every job subscribes to 'kill' message using Node Redis pub/sub. When the Web server sends a 'kill' message
 * all the processes in the process tree created by the job is killed.
 *
 */
var kue = require('kue');
var request = require('request');
var OZONEAPI  = require('./ozoneAPI').ozoneAPI;
var ozoneAccessToken = null;

const NodeCache = require( "node-cache" );
const myCache = new NodeCache();

// handle command line parameters
const commandLineArgs = require('command-line-args');
const optionDefinitions = [
  { name: 'host', alias: 'h', type: String },
  { name: 'port', type: Number, defaultOption: 6379 },
  { name: 'password', alias: 'p', type: String }
];
const options = commandLineArgs(optionDefinitions);

var config = {
  host  : options.host  , // Host of your locally running Redis server
  port  : options.port  , // Port of your locally running Redis server
  scope : 'kue',  // Use a scope to prevent two NRPs from sharing messages
  auth: options.password
};

var queue = kue.createQueue({redis:config});


var parallelJobs = 1;

/**
 * Kue Processor - Process Jobs
 * JOB TYPE - Job Status Update - Update status of Ansible jobs
 */
queue.process('statusUpdate', parallelJobs, function(job, ctx, done){

  job.removeOnComplete( true ).save()

  // Domain wrapper to handle uncaught exceptions and prevent jobs stuck in active state
  var domain = require('domain').create();
  domain.on('error', function(err){
    done(err);
  });
  domain.run(function(){ // your process function
    var ozoneHost = job.data.ozone_host;
    var ozonePort = job.data.ozone_port;
    var ozoneUsername = job.data.ozone_username;
    var ozonePassword = job.data.ozone_password;
    var ozoneAnsibleId = job.data.ozone_ansible_id;

    var ansibleObjectUpdate = job.data.ansibleObjectUpdate;

    var ozoneAPI = OZONEAPI(ozoneHost, ozonePort, ozoneUsername, ozonePassword, ozoneAccessToken);

    if(!ozoneAnsibleId){
      console.log("No ozoneAnsibleId. Exiting job");
      job.attempts(0);
      throw new Error(JSON.stringify('No Ozone Ansible Workflow ID to update. Killing job'));
    }

    let time = new Date().toISOString();
    job.log('%s - Updating Ansible Job %s - %s', time, ozoneAnsibleId, ansibleObjectUpdate);

    //Update ansible job
    ozoneAPI.updateAnsibleJob(ozoneAnsibleId, ansibleObjectUpdate,
      function(successResponse, accessToken){
        let time = new Date().toISOString();
        job.log('%s - Updated Ansible Job', time);
        console.log('%s - Updated Ansible Job', time);
        ozoneAccessToken = accessToken;
        done(null, 'Successfully updated Ansible Job!');

      }, function(errorResponse){
        let time = new Date().toISOString();
        job.log('%s - Error - Updating Ansible Job - %s', time, JSON.stringify(errorResponse));
        console.log('%s - Error - Updating Ansible Job - %s', time, JSON.stringify(errorResponse));
        throw new Error(JSON.stringify(errorResponse));
      });
  });

});

console.log("Started Queue Task Status Processor and waiting for jobs. Will process %s jobs in parallel", parallelJobs);

// Prevent Stuck jobs
queue.watchStuckJobs(1000);
