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


exports.getLogs = function(logfilename,successCallback,errorCallback){
  var logFile = 'logs/monitor/' + logfilename;
  var fs = require('fs');
  fs.readFile(logFile, function(err, data){
    if(err){
      errorCallback(err);
    }else{
      successCallback(data);
    }

  });
};

exports.execute = function(command,user,logfilename,dataCallback,completeCallback,errorCallback){
  var logFile = 'logs/monitor/' + logfilename;

  var fs = require('fs');
  fs.appendFile(logFile,command);

  //return completeCallback(command);

  ssh2_exec.executeCommand(user, command, logFile,
    function(data){
      //Partial Data
      //console.log("Data = "+ data)
      console.log("---------DataCallback");
      dataCallback(data)
    },
    function(data){
      //Complete Data
      console.log("---------CompleteCallback");
      completeCallback(data)
    },
    function(error){
      //Error Data
      //console.log("Error =" + error)
      console.log("---------ErrorCallback");
      errorCallback(error)
    }
  )
};

exports.monitor = function(user,monitorData,logfilename,dataCallback,completeCallback,errorCallback){
  var type = monitorData.type;
  var command = '';

  console.log("Type=" + type + " commandType=" + monitorData.commandType);

  if(monitorData.commandType === 'version' && ['vmware_vro','vmware_vra','vmware_vrops','vmware_vrapp','vmware_vrb','vmware_loginsight'].indexOf(type) > -1){
    return this.getVMVersionFromvCenter(user,type,monitorData.project.components,logfilename,dataCallback,completeCallback,errorCallback);
  }

  if(type === 'vipr') {
    this.monitorViPR(user, monitorData.commandType, monitorData.project.components.vipr, logfilename, dataCallback,completeCallback,errorCallback)
  }else if(type === 'vmware_vro'){
    this.monitorVRO(user,monitorData.commandType, monitorData.project.components,logfilename, dataCallback,completeCallback,errorCallback)
  }else if(type === 'vcenter'){
    this.monitorVcenter(user,monitorData.commandType, monitorData.project.components,logfilename, dataCallback,completeCallback,errorCallback)
  }else if(type === 'ssl_certs'){
    this.monitorSSLCerts(user, monitorData.URL ,dataCallback,completeCallback,errorCallback)
  }else{
    console.error("Invalid Monitor Type -" + type);
    errorCallback("Invalid Monitor Type -" + type)
  }

};

exports.monitorSSLCerts = function(user, URL, dataCallback,completeCallback,errorCallback){
  var command = 'echo | openssl s_client -connect ' + URL.replace("https://","").replace("http://","") + ' 2>/dev/null | openssl x509 -noout -issuer -subject -dates ' ;
  console.log("Command = " + command);
  var logfilename = 'check_ssl_certs.log';
  this.execute(command,user,logfilename,dataCallback,completeCallback,errorCallback)
};

exports.monitorViPR = function(user,commandType,vipr,logfilename, dataCallback,completeCallback,errorCallback){

  var command = config.scriptEngine.monitor + ' vipr ' + commandType + ' ' +
    '--user="root" '+
    '--ip='+ vipr.network_1_ipaddr + ' '+
    '--pass='+ vipr.password + ' ';

  console.log('ViPR Command =' + command);

  this.execute(command,user,logfilename,dataCallback,completeCallback,errorCallback)

};


exports.monitorVRO = function(user,commandType,components,logfilename,dataCallback,completeCallback,errorCallback){

  var command = config.scriptEngine.monitor + ' vro ' + commandType + ' ' +
    '--vro_host="' + components.vmware_vro.ip0 + '" '+
    '--vro_root_password="' + components.vmware_vro.varoot_password + '" ';

  exports.execute(command,user,logfilename,dataCallback,completeCallback,errorCallback)

};

exports.monitorVcenter = function(user,commandType,components,logfilename,dataCallback,completeCallback,errorCallback){

  var command = config.scriptEngine.monitor + ' vcenter ' + commandType + ' ' +
    '--ip="' + components.vcenter.host + '" '+
    '--username="' + components.vcenter.username + '" '+
    '--password="' + components.vcenter.password + '" ';

  console.log("Command = " + command);

  exports.execute(command,user,logfilename,dataCallback,completeCallback,errorCallback)

};

exports.getVMVersionFromvCenter = function(user,componentType,components,logfilename,dataCallback,completeCallback,errorCallback){
  //vcenter VMversion --ip="lglas073.lss.emc.com" --username="administrator@vsphere.local" --password="P@ssw0rd@123" --component_type="vmware_vro" --component_vmid="vim.VirtualMachine:vm-78"

  if(!components[componentType].vmid){
    return errorCallback("Cannot get version as VMID is not set")
  }

  var command = config.scriptEngine.monitor + ' vcenter VMversion ' +
    '--ip="' + components.vcenter.host + '" '+
    '--username="' + components.vcenter.username + '" '+
    '--password="' + components.vcenter.password + '" '+
    '--component_type="' + componentType + '" ' + '' +
    '--component_vmid="' + components[componentType].vmid + '" ';

  console.log("Command = " + command);

  exports.execute(command,user,logfilename,dataCallback,completeCallback,errorCallback)

};

