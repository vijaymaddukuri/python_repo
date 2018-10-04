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
 * @name upgradeTool
 * @description Module to Upgrade Ozone Web Framework and Scripts by downloading latest code from repository and building using grunt
 */
var ssh2_exec = require('../ssh/ssh2_exec');
var config =  require('../../config/environment');

/**
 * Get Upgrade Logs
 * @function
 * @param {string} logfilename
 * @param {callback} successCallback
 * @param {callback} errorCallback
 */
exports.getLogs = function(logfilename,successCallback,errorCallback){

  var logFile = '/opt/ozone-scripts/ehc-python-modules/logs/' + logfilename;
  var command = 'cat ' +logFile;

  var logFileData = '';

  console.log("Command = " + command);

  var localLogFile = 'logs/upgrade/upgrade.log';

  ssh2_exec.executeCommand(null, command, localLogFile,
    function(data){
      //Partial Data
      //console.log("Data = "+ data)
      //logFileData+=data
    },
    function(data){
      //Complete Data
      //console.log("Data =" + data)
      if(data)
      logFileData+=(data.toString().replace('Stream :: close :: code: 0, signal: undefined',''));
      console.log("Success Callback =" + logFileData);
      successCallback(logFileData)
    },
    function(error){
      //Error Data
      //console.log("Error =" + error)
      if(error)
      logFileData+=error;
      console.log("Error Callback =" + logFileData);
      errorCallback(logFileData)
    }
  );

};

/**
 * Upgrade
 * @function
 * @param {Object} user
 * @param {Object} upgradeData
 * @param {string} logfilename
 * @param {callback} dataCallback
 * @param {callback} completeCallback
 * @param {callback} errorCallback
 */
exports.upgrade = function(user,upgradeData,logfilename,dataCallback,completeCallback,errorCallback){
  var command = '/opt/ozone-scripts/ehc-python-modules/bin/ozone_upgrade.sh --force --restart > /opt/ozone-scripts/ehc-python-modules/logs/' + logfilename + " 2> >(sed $'s,.*,\\e[31m&\\e[m,'>&1)";

  var logFile = 'logs/upgrade/' + logfilename;

  var fs = require('filendir');

  fs.writeFile(logFile,command,{'flag':'a'});
  //return completeCallback(command);

  ssh2_exec.executeCommand(user, command, logFile,
    function(data){
      //Partial Data
      //console.log("Data = "+ data)
      completeCallback(data)
    },
    function(data){
      //Complete Data
      //console.log("Data =" + data)
      completeCallback(data)
    },
    function(error){
      //Error Data
      //console.log("Error =" + error)
      errorCallback(error)
    }
  )

};

/**
 * Get list of updates by checking for latest commits on git repository
 * @function
 * @param {object} user
 * @param {callback} dataCallback
 * @param {callback} completeCallback
 * @param {callback} errorCallback
 */
exports.checkUpdates = function(user,dataCallback,completeCallback,errorCallback){
  var command = '/opt/ozone-scripts/ehc-python-modules/bin/check_updates.sh';

  var logFile = 'logs/upgrade/check_updates.log';

  var fs = require('filendir');

  fs.writeFile(logFile,command,{'flag':'a'});
  //return completeCallback(command);

  ssh2_exec.executeCommand(user, command, logFile,
    function(data){
      //Partial Data
      //console.log("Data = "+ data)
      dataCallback(data)
    },
    function(data){
      //Complete Data
      //console.log("Data =" + data)
      completeCallback(data)
    },
    function(error){
      //Error Data
      //console.log("Error =" + error)
      errorCallback(error)
    }
  )

};
