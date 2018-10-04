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

var forever = require('../forever/forever');
var redis = require('../messaging/redis');

process.env.NODE_ENV = 'development';
//var envconfig = require('../../config/environment');
var envconfig = require('../../config/environment/shared');
var async = require('async');
var ssh2_exec = require('../ssh/ssh2_exec');
var logFile = 'logs/ansible/general.log';
var encryption = require('../../components/encrypt/encrypt');

/**
 * Writing a function to get list of services with latest master password in memory
 * @returns {[*,*,*,*]}
 */
var listOfServices = function(){

  var redisUrl = 'redis://' + global.serverCache.get('masterPassword') + '@' + envconfig.redis.host + ':' + envconfig.redis.port;

  return [
    {
      id: 'kue',
      append: true,
      outFile: '/data/log/ozone/kue/kue.log',
      logFile: '/data/log/ozone/kue/forever.log',
      sourceDir: '/opt/kue',
      workingDir: '/opt/kue',
      pidFile: '/var/run/kue.pid',
      script: 'node_modules/kue/bin/kue-dashboard',
      args: ['-p', '3000', '-r', redisUrl]
    },
    {
      id: 'kueCmdProcessor',
      append: true,
      outFile: '/data/log/ozone/kueCmdProcessor/kueProcessor.log',
      logFile: '/data/log/ozone/kueCmdProcessor/forever.log',
      sourceDir: '/opt/web/server/components/kue',
      workingDir: '/opt/web/server/components/kue',
      pidFile: '/var/run/kueCmdProcessor.pid',
      script: 'kueCmdProcessor.js',
      args: ['--host', envconfig.redis.host, '--port', envconfig.redis.port, '--password', global.serverCache.get('masterPassword')]
    },
    {
      id: 'kueTaskStatusProcessor',
      append: true,
      outFile: '/data/log/ozone/kueTaskStatusProcessor/kueProcessor.log',
      logFile: '/data/log/ozone/kueTaskStatusProcessor/forever.log',
      sourceDir: '/opt/web/server/components/kue',
      workingDir: '/opt/web/server/components/kue',
      pidFile: '/var/run/kueTaskStatusProcessor.pid',
      script: 'kueTaskStatusProcessor.js',
      args: ['--host', envconfig.redis.host, '--port', envconfig.redis.port, '--password', global.serverCache.get('masterPassword')]
    },
    {
      id: 'grunt-script.sh',
    }
  ];
};


/**
 * Get Services List
 * @param successCallback
 * @param errorCallback
 */
exports.getServiceList = function (successCallback, errorCallback) {

  // Run health check in parallel
  async.parallel({
    forever: function (callback) {
      var results = {};
      // Get forever task list - kueDashboard, kueCMDProcessor, kueTaskProcessor, OzoneWebServer
      forever.getTaskList(
        function (foreverTaskList) {

          // Filter through list of services defined
          results.data = listOfServices().map(item => {
            var foreverTask = foreverTaskList.filter(foundService => {
              return (item.id === foundService.id || item.id === foundService.file)
            });
            return foreverTask && foreverTask.length && foreverTask[0] || item
          });

          results.state = true;
          callback(null, results);

        }, function (err) {
          // Error Callback
          results.data = err;
          results.state = false;
          callback(null, results);
        });

    },
    redis: function (callback) {
      var results = {};
      redis.getServerInfo(
        function (redisResults) {
          results.data = redisResults;
          results.state = true;
          callback(null, results);
        }, function (err) {
          results.data = err;
          results.state = false;
          callback(null, results);
        })
    }
  }, function (err, results) {

    if (err) {
      errorCallback(err);
    } else {
      successCallback(results);
    }

  });

};


/**
 * Start Forever Tasks
 * Check if forever tasks are running already, if not start them
 */
var startForeverTasks = function(){

  // Check for existing forever tasks list and start if it is not started already
  forever.getTaskList(
    function (foreverTaskList) {

      // Filter through list of services defined
      listOfServices().map(item => {
        var foreverTask = foreverTaskList.filter(foundService => {
          return (item.id === foundService.id || item.id === foundService.file)
        });

        if (!foreverTask.length && item.script) {
          // Start the task if it does not already exist or task exists but is not running and script file exists
          require('forever').startDaemon(item.script, item);
        } else if (foreverTask) {
          console.log("Not starting service as it is already started")
        }

      });

    }, function (err) {
      // Error Callback
      console.error("Error getting list of forever tasks " + err)
    });
};

/**
 * Start Services
 * 1. Start Redis Server
 * 2. If success start Forever Tasks
 * @param successCallback
 * @param errorCallback
 */
exports.startServices = function (successCallback, errorCallback) {

  try {

    // Check for existing redis server by attempting to establish a connectivity. If not start redis server.
    exports.startRedisService(global.serverCache.get('masterPassword'),
      function (response) {
        successCallback("Redis Service Success " + response);
        startForeverTasks();
      },
      function (response) {
        errorCallback("Redis Service Failed " + response);
        startForeverTasks();
      }
    );

  } catch (e) {
    errorCallback("Error starting services " + e)
  }

};



/**
 * Start Redis Service - Check existing redis service and start if not running already
 * @param REDIS_PASSWORD
 * @param completeCallback
 * @param errorCallback
 */
exports.startRedisService = function (REDIS_PASSWORD, completeCallback, errorCallback) {

  // Security Workaround for storing redis password in conf file
  // Redis stores password in clear text format. So here we replace the conf file with password,
  // Start the service and replace back the password in conf file

  console.log("Checking for redis service");

  var script =
    "sed -i 's/requirepass .*/requirepass " + REDIS_PASSWORD + "/' /etc/redis.conf;" +
    'redis-server /etc/redis.conf;' +
    "sed -i 's/requirepass .*/requirepass PASSWORD_REMOVED/' /etc/redis.conf";

  console.log("Checking for redis service");

  redis.getServerInfo(
    function (redisResults) {
      errorCallback("Redis server already running")
    }, function (err) {
      console.error(err);
      if(err.toString().indexOf('ECONNREFUSED') > -1){
        console.log("<--------------- Starting redis server --------->");
        ssh2_exec.executeCommand(null, script, logFile, null,
          function (response) {
            console.log("<--------------- Success starting redis server --------->");
            completeCallback(response);
          },
          function (errorResponse) {
            console.log("<--------------- Error starting redis server --------->");
            errorCallback(errorResponse);
          });
      }else{
        errorCallback("Redis server may be running " + err);
      }
    });

};


/**
 * Check Agent Connectivity
 */
exports.checkAgentConnectivity = function(successCallback, errorCallback){
  var NRP = require('node-redis-pubsub');

  if(!global.serverCache.get('masterPassword')){
    return errorCallback("Master password not set")
  }

  envconfig.redis.auth = global.serverCache.get('masterPassword');

  var nrp_config = JSON.parse(JSON.stringify(envconfig.redis));
  nrp_config.scope = 'python';

  var nrp;

  try{
    nrp = new NRP(nrp_config);
  }catch(e){
    console.error("Unable to connect to Node Redis Pubsub");
    return errorCallback(e)
  }

  var responseSent = false;

  nrp.on('error', function (err) {
    if (!responseSent) {
      console.log("Killing heart beat listener");
      errorCallback('Error getting information from agent' + err);
      responseSent = true;
      nrp.quit();
    }
  });

  // Wait for info response
  nrp.on('heartBeatResponse', function (data) {
    //console.log("Received message " + data.logs);
    if (!responseSent) {
      successCallback(data);
      responseSent = true;
      nrp.off('heartBeatResponse');
      nrp.quit();
    } else {
      console.log("Response already sent")
    }

  });

  // Publish message requesting information
  nrp.emit('heartbeat', '');

  // Kill after 20 seconds
  setTimeout(function () {
    if (!responseSent) {
      console.log("Killing heartbeat listener");
      errorCallback('Couldn\'t retrieve agent heartbeat in 20 seconds. Check if the agent is running on the windows server.');
      responseSent = true;
      nrp.off('heartBeatResponse');
      nrp.quit();
    }
  }, 20000);
};


/**
 * Send Email Notification Via Agent
 * Note: It is also possible to send direct email notification from Ozone. Due to connectivity issues from docker to outside, using this method for now.
 * @param smtpDict
 * @param encryptionKey
 * @param successCallback
 * @param errorCallback
 * @returns {*}
 */
exports.sendEmailNotificationViaAgent = function(smtpDict, encryptionKey, successCallback, errorCallback){
  console.log("send email notification via agent");

  console.log("smtp Dict" + JSON.stringify(smtpDict));

  console.log("smtpDict == True" + (smtpDict.auth_required == true));

  var NRP = require('node-redis-pubsub');

  if(!global.serverCache.get('masterPassword')){
    console.error("Master password not set");
    return errorCallback("Master password not set")
  }

  envconfig.redis.auth = global.serverCache.get('masterPassword');

  var nrp_config = JSON.parse(JSON.stringify(envconfig.redis));
  nrp_config.scope = 'python';

  var nrp;

  try{
    nrp = new NRP(nrp_config);
  }catch(e){
    console.error("Unable to connect to Node Redis Pubsub");
    return errorCallback(e)
  }

  console.error("Here");

  var responseSent = false;

  nrp.on('error', function (err) {
    console.error("Error on NRP " + err);
    if (!responseSent) {
      console.log("Killing email response listener");
      errorCallback('Error getting information from agent' + err);
      responseSent = true;
      nrp.quit();
    }
  });

  // Wait for info response
  nrp.on('results:emailResponse', function (data) {
    //console.log("Received message " + data.logs);
    if (!responseSent) {
      successCallback(data);
      responseSent = true;
      nrp.off('results:emailResponse');
      nrp.quit();
    } else {
      console.log("Response already sent")
    }

  });


  var emailData = {
    'module_name': "preDeploymentValidation.validateSMTP",
    'method_name': "validateSMTP",
    'method_params': {
      targetHost: smtpDict.server,
      tcpPorts: [ smtpDict.port ],
      sendMailConfDict: {
        smtpServer: smtpDict.server,
        smtpPort: smtpDict.port,
        senderMailID: smtpDict.auth_required == "true" && smtpDict.username || smtpDict.sender_address,
        senderPassword: smtpDict.auth_required == "true" && encryption.decrypt(smtpDict.password, encryptionKey) || "",
        recieverMailID: smtpDict.receiver_address,
        subject: 'FAILED - EHC Automated Install Failed',
        textInMail: 'Playbook execution failed. Please login to the portal and check for more information.'
      }

    },
    'unique_id': 'emailResponse',
    'no_log': false
  };

  console.log(JSON.stringify(emailData));

  // Publish message requesting information
  nrp.emit('run', emailData);

  // Kill after 60 seconds
  setTimeout(function () {
    if (!responseSent) {
      console.log("Killing Email Response");
      errorCallback('Couldn\'t retrieve Email Response in 20 seconds. Check if the agent is running on the windows server.');
      responseSent = true;
      nrp.off('results:emailResponse');
      nrp.quit();
    }
  }, 60000);
};

// exports.getServiceList();

// console.log(exports.startServices('P@ssw0rd@123', function(response){
//   console.log("Response")
// },function(response){
//   console.error("Response")
//   }
// ));
