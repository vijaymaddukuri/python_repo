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


var ssh2_exec = require('../ssh/ssh2_exec');
var scp2_exec = require('../scp/scp_exec');
var config =  require('../../config/environment');
var encryption = require('../../components/encrypt/encrypt');
var kueapi = require('../../components/kue/kueAPI').kueAPI();

/**
 * Get Logs from Kue Job Processor
 * @param entity
 * @param successCallback
 * @param errorCallback
 */
exports.getLogs = function(entity,successCallback,errorCallback) {
  console.log("Getting job id - " + entity.jobId)
  kueapi.getJobLogs(entity.jobId,function(response){
    successCallback(response)
  },function(response){
    errorCallback(response)
  });
};

/*exports.getLogs_old = function(logfilename,successCallback,errorCallback){
  var logFile = 'logs/snapshot/' + logfilename;
  var fs = require('fs');
  fs.readFile(logFile, function(err, data){
    if(err){
      errorCallback(err);
    }else{
      successCallback(data);
    }

  });
};*/

/**
 * Run Job using Kue Processor
 * @param snapJobObject
 * @param command
 * @param user
 * @param logfilename
 * @param completeCallback
 * @param errorCallback
 */
exports.runJob = function(snapJobObject,command,user,logfilename,completeCallback,errorCallback,title){

  try{
    kueapi.runJob({
      type:'exec',
      data:{
        title: title,
        "command": command,
        "id" : snapJobObject._id
      }
    },function(response){
      completeCallback(response)
    },function(response){
      errorCallback(response)
    });

  }catch(e){
    errorCallback(e);
  }
};

/**
 * Execute a command directly over SSH
 * @param command
 * @param user
 * @param logfilename
 * @param completeCallback
 * @param errorCallback
 */
exports.execute = function(command,user,logfilename,completeCallback,errorCallback){
  var logFile = 'logs/snapshot/' + logfilename;

  var fs = require('filendir');
  fs.writeFile(logFile,command,{'flag':'a'});

  ssh2_exec.executeCommand(user, command, logFile,
    null,
    function(data){
      completeCallback(data)
    },
    function(error){
      errorCallback(error)
    }
  )
};

/**
 * Snapshot Configure Actions - List, Create, Delete, Revert
 * @param snapJobObject
 * @param user
 * @param configData
 * @param logfilename
 * @param completeCallback
 * @param errorCallback
 */
exports.configure = function(snapJobObject, user,configData,logfilename,completeCallback,errorCallback){
  var type = configData.type; // vipr, vro, vcenter . Doensnt matter here
  var vmid = configData.vmid;
  var operation = configData.operation; // create, list, revert
  var snapshotname = configData.snapshotname;
  var snapshotdescription= configData.snapshotdescription;
  var shutdownGuest= configData.shutdownGuest;

  if(operation === 'create') {
    this.createSnapshot(snapJobObject, user, configData, vmid, snapshotname, snapshotdescription, shutdownGuest, logfilename, completeCallback,errorCallback)
  }else if(operation === 'list'){
    this.listSnapshot(user, configData, vmid, snapshotname, snapshotdescription, logfilename, completeCallback,errorCallback)
  }else if(operation === 'revert'){
    this.revertSnapshot(snapJobObject, user, configData, vmid, configData.snapshotId, snapshotdescription, logfilename, completeCallback,errorCallback)
  }else if(operation === 'delete'){
    this.deleteSnapshot(snapJobObject, user, configData, vmid, configData.snapshotId, snapshotdescription, logfilename, completeCallback,errorCallback)
  }else{
    errorCallback("Invalid Config Type -" + type)
  }

};


/**
 * Get vCenter Connection Info
 * @param configData
 * @returns {string}
 */
exports.getConnectionInfo = function(configData){

  var common = configData.project.components.import_data.vars.common;

  if(common.external_vcenter_hostname)
    return '--ip="' + common.external_vcenter_hostname + '" '+
      '--username="' + common.external_vcenter_administrator_username + '" '+
      '--password="' + encryption.decrypt(common.external_vcenter_administrator_password, configData.project.components.encryptionKey) + '" ';

  return '--ip="' + common.cloud_vcenter_hostname + '" '+
    '--username="' + common.cloud_vcenter_administrator_username + '" '+
    '--password="' + encryption.decrypt(common.cloud_vcenter_administrator_password, configData.project.components.encryptionKey) + '" ';
};

/**
 * Create Snapshot
 * @param snapJobObject
 * @param user
 * @param configData
 * @param vmid
 * @param snapshotname
 * @param snapshotdescription
 * @param shutdownGuest
 * @param logfilename
 * @param completeCallback
 * @param errorCallback
 */
exports.createSnapshot = function(snapJobObject, user,configData, vmid, snapshotname, snapshotdescription, shutdownGuest, logfilename, completeCallback,errorCallback){

  var command = config.scriptEngine.snapshot + ' create '+
    '--vmid=' + vmid  + ' ' +
    '--snapname="' + snapshotname + '" ' +
    '--description="' + snapshotdescription + '" ' +
    '--logfile="'+logfilename.replace('.log','') + '" ';

  if(shutdownGuest === 'Shutdown'){
    command +=  '--shutdown_guest '
  }

  command += this.getConnectionInfo(configData);

  this.runJob(snapJobObject, command,user,logfilename,completeCallback,errorCallback,'Create Snapshot for VMID -' + vmid + ' - name ' + snapshotname)

};

/**
 * List Snapshot
 * @param user
 * @param configData
 * @param vmid
 * @param snapshotname
 * @param snapshotdescription
 * @param logfilename
 * @param completeCallback
 * @param errorCallback
 */
exports.listSnapshot = function(user,configData, vmid, snapshotname, snapshotdescription, logfilename, completeCallback,errorCallback){


  var command = config.scriptEngine.snapshot + ' list '+
    '--vmid=' + vmid  + ' ' +
    '--snapname=' + snapshotname + ' ' +
    '--logfile="'+logfilename.replace('.log','') + '" ';

  command += this.getConnectionInfo(configData);

  this.execute(command,user,logfilename,completeCallback,errorCallback)

};

/**
 * Revert Snapshot
 * @param snapJobObject
 * @param user
 * @param configData
 * @param vmid
 * @param snapshotId
 * @param snapshotdescription
 * @param logfilename
 * @param completeCallback
 * @param errorCallback
 */
exports.revertSnapshot = function(snapJobObject, user,configData, vmid, snapshotId, snapshotdescription, logfilename, completeCallback,errorCallback){


  var command = config.scriptEngine.snapshot + ' revert '+
    '--vmid=' + vmid  + ' ' +
    '--snapshot_id=' + snapshotId + ' ' +
    '--logfile="'+logfilename.replace('.log','') + '" ';

  command += this.getConnectionInfo(configData);

  this.runJob(snapJobObject, command,user,logfilename,completeCallback,errorCallback,'Revert Snapshot for VMID -' + vmid + ' - name ' + snapshotId)

};

/**
 * Delete Snapshot
 * @param snapJobObject
 * @param user
 * @param configData
 * @param vmid
 * @param snapshotId
 * @param snapshotdescription
 * @param logfilename
 * @param completeCallback
 * @param errorCallback
 */
exports.deleteSnapshot = function(snapJobObject, user,configData, vmid, snapshotId, snapshotdescription, logfilename, completeCallback,errorCallback){

  var command = config.scriptEngine.snapshot + ' delete '+
    '--vmid=' + vmid  + ' ' +
    '--snapshot_id=' + snapshotId + ' ' +
    '--logfile="'+logfilename.replace('.log','') + '" ';

  command += this.getConnectionInfo(configData);

  this.runJob(snapJobObject, command,user,logfilename,completeCallback,errorCallback,'Delete Snapshot for VMID -' + vmid + ' - name ' + snapshotId)

};
