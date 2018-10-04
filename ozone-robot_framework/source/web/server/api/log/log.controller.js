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
 * Using Rails-like standard naming convention for endpoints.
 * GET     /api/logs              ->  index
 * POST    /api/logs              ->  create
 * GET     /api/logs/:id          ->  show
 * PUT     /api/logs/:id          ->  update
 * DELETE  /api/logs/:id          ->  destroy
 */

'use strict';

import _ from 'lodash';
import Log from './log.model';
import Project from '../project/project.model';

var envconfig =  require('../../config/environment');

var logFileLocations = {
  'redis': '/var/log/redis.out',
  'kue':'/data/log/ozone/kue/forever.log',
  'kueCmdProcessor':'/data/log/ozone/kueCmdProcessor/forever.log',
  'kueTaskStatusProcessor':'/data/log/ozone/kueTaskStatusProcessor/forever.log'
};

// Gets a list of Logs
export function index(req, res) {
  var read = require('fs-readdir-recursive');
  res.send(read('logs'));
}

// Gets a single Log from the DB
export function show(req, res) {

  console.log("Read file " + 'logs\\'+req.body.filePath);

  var fs = require('fs');
  fs.readFile('logs/'+req.body.filePath, function(err, data){
    if(err){
      res.status(500).send(err)
    }else{
      res.send(data);
    }

  });

}


function handleEntityNotFound(res) {
  return function(entity) {
    if (!entity) {
      res.status(404).end();
      return null;
    }
    return entity;
  };
}

function handleError(res, statusCode) {
  statusCode = statusCode || 500;
  return function(err) {
    res.status(statusCode).send(err);
  };
}


/**
 * read local Log File
 * @param req
 * @param res
 */
var readLocalLogFile = function(req, res, type, lines){

  console.log('Fethincg logs from %s', logFileLocations[type]);


  var ssh2_exec = require('../../components/ssh/ssh2_exec');
  var command = "tail -" + lines + " " + logFileLocations[type];
  ssh2_exec.executeCommand(req.user.name, command, null,
    function(data){

    },
    function(data){
      //Complete Data
      res.send(data)
    },
    function(error){
      //Error Data
      res.status(500).send(error)
    }
  );
};

/**
 * Get FEHC Logs
 * @param req
 * @param res
 */
var fetchAgentLogs = function(req, res, lines){

  var fs = require('filendir');
  var logFile = 'logs/fehc.log';

  var NRP    = require('node-redis-pubsub');

  var nrp_config = envconfig.redis;
  nrp_config.auth = global.serverCache.get('masterPassword');
  nrp_config.scope = 'python';

  var nrp = new NRP(nrp_config);

  var responseSent = false;

  nrp.on('error', function(err){
    if(!responseSent) {
      console.log("Killing log listener");
      res.status(500).send('Error listening for Python Logs ' + err);
      responseSent = true;
      nrp.quit();
    }
  });

  nrp.on('logResults', function(data){
    //console.log("Received message " + data.logs);
    if(!responseSent){
      res.send(data.logs);
      responseSent = true;
      nrp.off('logResults');
      fs.writeFile(logFile,data.logs,{'flag':'w'});
      nrp.quit();
    }else{
      console.log("Response already sent")
    }

  });

  console.log("emitting for logs")
  nrp.emit('logs', lines);

  setTimeout(function () {
    if(!responseSent){
      console.log("Killing log listener");
      res.status(500).send('Couldnt retreive logs in given time');
      responseSent = true;
      nrp.off('logResults');
      nrp.quit();
    }
  }, 60000);
};


/**
 * Get vRA Logs
 * @param {Object} req API Request containing project data
 * @param {Object} res API Request contains vRA logs
 */
var getvRALogs = function(project, req, res){
  var encryption = require('../../components/encrypt/encrypt');

  var vra_host = project.components.import_data.vars.host_address.vra_primary.ip;

  var scriptEngineConfig = {
    host: vra_host,
    port: 22,
    user: 'root',
    tryKeyboard: true,
    password: encryption.decrypt(project.components.import_data.vars.vrealize_automation.vra_root_password, project.components.encryptionKey)
  };

  // var command = 'cat /var/log/vmware/vcac/vra-ha-config.log';
  var command = "cd /tmp/ && cat `ls -t /tmp/ | grep EHCAuto | head -1`";

  var ssh2_exec = require('../../components/ssh/ssh2_exec');
  ssh2_exec.executeCommand(req.user.name, command, null,
    function(data){
      //Partial Data
      //console.log("Data = "+ data)

    },
    function(data){
      //Complete Data
      //console.log("Data =" + data)
      res.send(data)
    },
    function(error){
      //Error Data
      //console.log("Error =" + error)
      res.status(500).send(error)
    },null,scriptEngineConfig
  )

};

/**
 * Get Python Logs
 * @param req
 * @param res
 */
export function service(req, res) {

    var type = req.params.type;
    var lines = req.params.lines;

    if(type === 'agent'){
      fetchAgentLogs(req, res, lines);
    }
    else{
      readLocalLogFile(req, res, type, lines);
    }

}

/**
 * vRA Logs
 * @param req
 * @param res
 */
export function vRALogs(req, res){
  // Exceptional case
  // vRA host name is required for vRA Logs. Get vRA Hostname from project data
  var projectid = req.params.projectid;

  Project.findById(projectid)
    .then(handleEntityNotFound(res))
    .then(function(entity){
      getvRALogs(entity, req, res)
    })
    .catch(handleError(res));
}
