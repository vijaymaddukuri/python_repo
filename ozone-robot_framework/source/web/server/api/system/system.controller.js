/**
 * Using Rails-like standard naming convention for endpoints.
 * GET     /api/system              ->  index
 * POST    /api/system              ->  create
 * GET     /api/system/:id          ->  show
 * PUT     /api/system/:id          ->  update
 * DELETE  /api/system/:id          ->  destroy
 */

'use strict';

import _ from 'lodash';
import System from './system.model';

var envconfig = require('../../config/environment');
var kueAPI = require('../../components/kue/kueAPI');
var async = require('async');

// Deletes a System from the DB
export function startServices(req, res) {

  var masterPassword = global.serverCache.get('masterPassword');

  if(!masterPassword){
    res.status(500).send('Master Password not available');
  }else{

    // Require frameworkUtils here so it initializes the services list with master password
    var frameworkUtils = require('../../components/debug/framework');
    frameworkUtils.startServices(function(){
      res.send('Success')
    }, function(error){
      res.status(500).send(error);
    })
  }

}



/**
 * Set Master Password
 * @param req
 * @param res
 */
export function setMasterPassword(req, res){

  try{
    global.serverCache.set('masterPassword', req.body.masterPassword);
    envconfig.redis.auth = req.body.masterPassword;
    res.send();
  }catch(e){
    res.status(500).send(e);
  }

}

// Checks if Master password is set or not
export function masterPassword(req, res) {

  if(global.serverCache.get('masterPassword')){
    res.send('Master Password Set');
  }else {
    res.status(500).send('Master Password Not Set');
  }
}


// Gets a list of services
export function services(req, res) {
  var frameworkUtils = require('../../components/debug/framework');
  return frameworkUtils.getServiceList(
    function (data) {
      res.send(data);
    }, function (err) {
      res.status(500).send(err);
    })
}

/**
 * Get Agent details through heart beat
 * @param req
 * @param res
 */
export function agent(req, res) {

  var NRP = require('node-redis-pubsub');

  var nrp_config = JSON.parse(JSON.stringify(envconfig.redis));
  nrp_config.scope = 'python';

  var nrp;

  try{
    nrp = new NRP(nrp_config);
  }catch(e){
    console.error("Unable to connect to Node Redis Pubsub");
    return res.status(500).send(e)
  }

  var responseSent = false;

  nrp.on('error', function (err) {
    if (!responseSent) {
      console.log("Killing info listener");
      res.status(500).send('Error getting information from agent' + err);
      responseSent = true;
      nrp.quit();
    }
  });

  // Wait for info response
  nrp.on('infoResponse', function (data) {
    //console.log("Received message " + data.logs);
    if (!responseSent) {
      res.send(data);
      responseSent = true;
      nrp.off('infoResponse');
      nrp.quit();
    } else {
      console.log("Response already sent")
    }

  });

  // Publish message requesting information
  nrp.emit('info', '');

  // Kill after 10 seconds
  setTimeout(function () {
    if (!responseSent) {
      console.log("Killing info listener");
      res.status(500).send('Couldn\'t retrieve agent information in 10 seconds');
      responseSent = true;
      nrp.off('infoResponse');
      nrp.quit();
    }
  }, 10000);

}

/**
 * Get Queue Jobs
 * @param req
 * @param res
 */
export function queueJobs(req, res) {

  var kue = require('kue');
  var queue;

  queue = kue.createQueue({redis:{host: 'localhost', auth: global.serverCache.get('masterPassword')}});

  queue.on( 'error', function( err ) {
    console.log("Queue error " + err);
    console.log("Header sent =" + res.headersSent);
     !res.headersSent && res.status(500).send(err);
    return queue.shutdown(function(){
      console.log("Queue Shutdown");
    })
  });


  var getJobCountByType = function(type, callback){
    async.parallel({

      inactiveCount: function(execCallback){
        queue.inactiveCount(type, execCallback);
      },
      failedCount: function(execCallback){
        queue.failedCount(type, execCallback);
      },
      activeCount: function(execCallback){
        queue.activeCount(type, execCallback);
      },
      completeCount: function(execCallback){
        queue.completeCount(type, execCallback);
      }

    }, callback);
  };

  async.parallel({

    exec: function(callback){
      console.log("Getting Job Count by type");
      getJobCountByType('exec', callback);
    },
    statusUpdate: function(callback){
      console.log("Getting Job Count by type");
      getJobCountByType('statusUpdate', callback);
    }
  }, function(err, callback){
    console.log("response header sent =" + res.headersSent);
    console.log("response header sent not =" + !res.headersSent);
    queue.shutdown(function(){
      console.log("Shutdown")
    });
    if(err){
      !res.headersSent && res.status(500).send(err)
    }else{
      !res.headersSent && res.send(callback)
    }

  });

  /*

   var kueapi = kueAPI.kueAPI();

   kueapi.getStats(
   function (response) {
   res.send(response)
   }, function (response) {
   res.status(500).send(response)
   })*/

}

/**
 * Requeue jobs stuck in active state
 * NOTE: ONLY REQUEUE STATUSUPDATE JOBS. REQUEUING EXEC JOBS WILL RESULT IN RE-EXECUTING ANSIBLE JOBS
 * EXEC JOBS STUCK IN ACTIVE STATE MUST BE KILLED AFTER ENSURING THEY ARE STUCK
 * @param req
 * @param res
 */
export function requeue(req, res){

  var kue = require('kue');
  var queue;

  try{
    queue = kue.createQueue({redis:{auth: global.serverCache.get('masterPassword')}});
  }catch(e){
    return res.status(500).send(e)
  }

  queue.active( function( err, ids ) {
    ids.forEach( function( id ) {
      kue.Job.get( id, function( err, job ) {
        // Your application should check if job is a stuck one
        // NOTE: ONLY REQUEUE STATUSUPDATE JOBS. REQUEUING EXEC JOBS WILL RESULT IN RE-EXECUTING ANSIBLE JOBS
        if(job.type === "statusUpdate"){
          console.log("Re-queuing job " + id);
          job.inactive();
        }
      });
    });

    if(err){
      res.status(500).send(err);
    }else{
      res.send("Requeued " + ids.length + " jobs");
    }

  });

}


/**
 * Cleanup Queue
 */
export function cleanupQueue(req, res){

  var kue = require('kue');
  var queue;

  try{
    queue = kue.createQueue({redis:{auth: global.serverCache.get('masterPassword')}});


    kue.Job.rangeByType('statusUpdate', 'complete', 0, 10000, 'asc', function (err, jobs) {
      console.log("Jobs = ", jobs.length);
      jobs.forEach(function (job) {
        job.remove(function () {
          console.log('removed ', job.id);
        });
      });

      // TODO: Improve this in the future to use async series
      res.send("Cleaned up " + jobs.length + " jobs")

    });

  }catch(e){
    return res.status(500).send(e)
  }

}
