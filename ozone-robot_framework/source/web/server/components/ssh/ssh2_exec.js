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


var Client = require('ssh2').Client;

//var exec = require('ssh-exec');

var config = require('../../config/environment');
var logger = require('../Logger');

var serverLogger = logger.serverLogger;

/**
 * Execute Shell Command
 * @param user
 * @param command
 * @param logfilelocation
 * @param dataCallback
 * @param completeCallback
 * @param errorCallback
 * @param plainLogger
 * @param scriptEngine
 * @param decryptedVaultPassword
 */
exports.executeCommand = function(user, command,logfilelocation, dataCallback,completeCallback,errorCallback,plainLogger, scriptEngine, decryptedVaultPassword){

  var fs = require('filendir');
  var time = new Date().getTime();
  //var logFile = 'logs/deploy/' + logfilename;
  var logFile = logfilelocation;

  if(!scriptEngine) scriptEngine = {};

  var moduleLogger = logger.customLogger(logFile);

  if(plainLogger)
    moduleLogger = logger.plainLogger(logFile);

  var conn = new Client();

  var connHost = scriptEngine.host || config.scriptEngine.host;
  var connUser = scriptEngine.user || config.scriptEngine.user;
  var connHostPassword = scriptEngine.password || config.scriptEngine.password;

  var scriptEngineConfig = {
    host: connHost,
    port: 22,
    username: connUser,
    tryKeyboard: true
  };

  if(connHostPassword){
    scriptEngineConfig.password = connHostPassword;
  }else{
    scriptEngineConfig.privateKey = require('fs').readFileSync(config.scriptEngine.privateKey);
  }

  //fs.appendFile(logFile,command);
  // TODO: Remove this before production
  // console.log("Writing Command to log file =" + command);

  //Create folder directory structure if not exists
  if(logFile)
    fs.writeFile(logFile,"\n",{'flag':'a'});

  moduleLogger.info("\n");
  moduleLogger.info(hashPassword(command));

  conn.on('keyboard-interactive', function(name, instr, lang, prompts, cb) {
    cb([connHostPassword]);
  });

  conn.on('error', function(error) {
    console.log("SSH Connect Error" + error);
    errorCallback(error);
  });

  conn.on('ready', function() {

    conn.exec(command, function(err, stream) {
      var callBackSent = false;

      if (err) {
        console.log("Error=" + err);
        moduleLogger.error(err);
        errorCallback(err);

      }

      var error_data = "";
      var std_out = "";

      stream.on('close', function(code, signal) {
        moduleLogger.info("\n" + error_data.toString());
        moduleLogger.info('Stream :: close :: code: ' + code + ', signal: ' + signal);
        moduleLogger.info('OZONE_PROGRAM_COMPLETED');

        if(code === 0){
          completeCallback(std_out);
        }else{
          errorCallback(error_data)
        }

        conn.end();
      }).on('data', function(data) {
        serverLogger.debug(data.toString());
        std_out += data;
        moduleLogger.info(data.toString());

        if(dataCallback)
          dataCallback(data);

      }).stderr.on('data', function(data) {

        std_out += data;
        console.error('STDERR: ' + data);
        serverLogger.error(data.toString());
        error_data+=data;

      });

    });
  }).connect(scriptEngineConfig);
};

/**
 * Hash Password from log file
 * @param message
 * @returns {*}
 */
var hashPassword = function(message){

  var regex = /PASSWORD=(.*?);/g;
  var subst = `PASSWORD=NOTLOGGED;`;

  var result;

  // Remove password from log file
  if(message){
    result = message.toString().replace(regex, subst);
  }

  return result;

};
