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
var forever = require("forever");


/**
 * Get List of Forever Tasks Running
 * @param successCallback
 * @param errorCallback
 */
exports.getTaskList = function(successCallback, errorCallback){

  forever.list(false, function(err, processes){

    if(err){
      errorCallback(err);
    }else{
      successCallback(processes);
    }
    /*
    processes.map(function (proc) {
      console.log(proc.file + " " + proc.running);
    })*/
  });

};

/*

 // Test
 exports.getTaskList(function(response){

 console.log(response);

 });
*/
