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
 * @module
 * @name kueCmdProcessor
 * @description Kue Command Processor processes jobs submitted by Kue(Queue) from the web application.
 * Every job subscribes to 'kill' message using Node Redis pub/sub. When the Web server sends a 'kill' message
 * all the processes in the process tree created by the job is killed.
 *
 */
var kue = require('kue');
var kill = require('tree-kill');
var NRP    = require('node-redis-pubsub');

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


var parallelJobs = 20;

/**
 * Log to Kue Job
 * @param job
 * @param message
 */
var logToKue = function(job, message, outToConsole){

  var time = new Date().toISOString();
  var regex = /PASSWORD=(.*?);/g;
  var subst = `PASSWORD=NOTLOGGED;`;

  var result;

  // Remove password from log file
  if(message){
    result = message.toString().replace(regex, subst);
  }

  job.log('%s - %s', time, result);

  if(outToConsole)console.log('%s - %s', time, result);

};

/**
 * Execute Command
 * @param job
 * @param done
 */
var execCommand = function(job, done){
  var exec = require('child_process').exec;
  var child = exec(job.data.command, {maxBuffer: 1024*1024*50}, (error, stdout, stderr) => {
    if (error){
      logToKue(job, error, true);
    }
    if (stderr) {
      logToKue(job, stderr, true);
    }
  });

  var nrp = new NRP(config);

  logToKue(job, "Subscribing to stop ", true);
  nrp.on('stop', function(data){
    logToKue(job,"Received stop message. Checking if stop message is for this job. This job ID = " + job.id + " ; Stop Message job ID = " + data.jobid, true);
    if(parseInt(job.id) === parseInt(data.jobid)){
      logToKue(job, 'Stop message is for this job', true);
      logToKue(job, "Not Killing job " + data.jobid + " and waiting for Ansible to finish current Task", true);
    }
  });

  logToKue(job, "Subscribing to kill ", true);
  //Subscribe to 'kill' message
  nrp.on('kill', function(data){
    logToKue(job, "Received kill message. Checking if stop message is for this job. This job ID = " + job.id + " ; Stop Message job ID = " + data.jobid, true);
    if(parseInt(job.id) === parseInt(data.jobid)){
      logToKue(job, "Killing job " + data.jobid + " and not waiting for Ansible to finish current Task", true);
      kill(child.pid);
      nrp.off('kill');
      nrp.quit();
      throw new Error('Stopped on demand');
    }
  });

  // On data from the job log to job logs
  child.stdout.on('data', function(chunk) {
    console.log("Data in kueCMDProcessor");
    logToKue(job, chunk);
  });

  // On error data log in Kue
  child.stderr.on('data', function(chunk) {
    console.log("error Data in kueCMDProcessor");
    logToKue(job, chunk);
  });

  // Handle Error
  child.on('error', (err) => {
    console.log("ERROR in kueCMDProcessor");
    logToKue(job, err, true);
    nrp.off('kill');
    nrp.quit();
    throw new Error('Failed to start child process. -' + err);

  });

  // On Connection close
  // Update return code
  // Quit messaging subscriber
  child.on('close', (code) => {

    logToKue(job, 'Return Code - ' + code, true);

    if(code !== 0){
      throw new Error('Process finished with return code -' + code);
    }else{
      done(null, 'Process finished!');
    }
    logToKue(job, "Quiting NRP messaging for job " + job.id, true);
    nrp.off('kill');
    nrp.quit();

  });
};

/**
 * Kue Processor - Process Jobs
 * JOB TYPE - EXEC - Execute a shell command
 */
queue.process('exec', parallelJobs, function(job, ctx, done){

  logToKue(job, "Received Job - %s", job.id, true);

  // Domain wrapper to handle uncaught exceptions and prevent jobs stuck in active state
  var domain = require('domain').create();
  domain.on('error', function(err){
    job.log('CMD Processor domain wrapper received error. Closing - %s' % err, true);
    done(err);
  });
  domain.run(function(){ // your process function
    execCommand(job, done);
  });

});

console.log("Started Queue CMD Processor and waiting for jobs. Will process %s jobs in parallel", parallelJobs);

// Prevent Stuck jobs
queue.watchStuckJobs(1000);
