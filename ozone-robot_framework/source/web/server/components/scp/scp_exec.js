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


var config = require('../../config/environment');
//var config = require('../../config/environment/development.js');
var client = require('scp2');
var logger = require('../Logger');
var serverLogger = logger.serverLogger;


exports.copyFileToScriptEngine = function(sourcePath,destinationPath){
  var scriptEngineConfig = {
    host: config.scriptEngine.host,
    port: 22,
    username: config.scriptEngine.user,
    tryKeyboard: true
  };

  serverLogger.info("Copy file to Script Engine -" + destinationPath);

  if(config.scriptEngine.password){
    scriptEngineConfig.password = config.scriptEngine.password;
  }else{
    scriptEngineConfig.privateKey = require('fs').readFileSync(config.scriptEngine.privateKey);
  }

  scriptEngineConfig.destinationPath = destinationPath;
  var Client = require('scp2').Client;
  var cl = new Client(scriptEngineConfig);

  cl.on('keyboard-interactive', function(name, instr, lang, prompts, cb) {
    cb([config.scriptEngine.password]);
  });

  cl.upload(sourcePath,destinationPath,function(err) {
    if(err){
      console.error(err)
    }else{
      console.log("Successfully uploaded file")
      cl.close()
    }
  })
};

exports.createFileOnScriptEngine = function(contents,destinationPath,successCallback,errorCallback){
  var Client = require('scp2').Client;
  var buffer = new Buffer(contents, "utf-8");

  var scriptEngineConfig = {
    host: config.scriptEngine.host,
    port: 22,
    username: config.scriptEngine.user,
    tryKeyboard: true
  };

  if(config.scriptEngine.password){
    scriptEngineConfig.password = config.scriptEngine.password;
  }else{
    scriptEngineConfig.privateKey = require('fs').readFileSync(config.scriptEngine.privateKey);
  }

  serverLogger.info("Create file on Script Engine -" + destinationPath);

  var cl = new Client(scriptEngineConfig);

  cl.on('keyboard-interactive', function(name, instr, lang, prompts, cb) {
    cb([config.scriptEngine.password]);
  });

  //TODO: handle "handle is not a Buffer" error
  //cl.connect(scriptEngineConfig);
  cl.on('error', function(error) {
    console.log("SSH Connect Error" + error);
    errorCallback(error);
  });

  cl.write({
    destination: destinationPath,
    content: buffer
  }, function(err){
    if(err){
      errorCallback(err);
      console.error(err)
    }else{
      console.log("Success SCP")
      successCallback()
    }
    cl.close()
  });

};

//exports.copyFileToScriptEngine('scp_exec.js','/tmp/ssh_tezt.js');
/*exports.createFileOnScriptEngine('sdfdddddddddsfd','/tmp/testfile.txt', function(response){
  console.log("Success" + response)
}, function(response){
  console.log("Error" + response)
});*/
