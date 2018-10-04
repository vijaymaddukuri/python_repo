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


var NRP    = require('node-redis-pubsub');

/**
 * Messaging using Node Redis PubSub
 */

function pubSub(){

  return{

    /**
     * Publish a message
     * @param type - Type of message to publish
     * @param data - Actual message in json format
     * @param successCallback - SuccessCallback
     * @param errorCallback - ErrorCallback
     * @param scope - Use scope to restrict messages between listeners. default is 'kue'. override if required.
     */
    emit: function(type, data, successCallback, errorCallback, scope){

      var config = require('../../config/environment').redis;
      config.auth = global.serverCache.get('masterPassword');

      if(scope){
        config.scope = scope;
      }

      console.log("Sending kill message " + JSON.stringify(config));
      console.log("Type =" + type);

      var nrp = new NRP(config);
      nrp.on("error", function(err){
        // Handle errors here
        console.log("Error NRP Messaging -" + err);
        errorCallback("Error NRP Messaging -" + err)
      });

      nrp.emit(type, data);
      //nrp.emit('pause', { jobid: 224 });

      nrp.quit();
      successCallback();

    }

  }

}

exports.pubSub = pubSub;
