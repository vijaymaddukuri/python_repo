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

var redis = require("redis");
var envconfig =  require('../../config/environment');

/**
 * Get Redis Service Details
 * @param successCallback
 * @param errorCallback
 */
exports.getServerInfo = function(successCallback, errorCallback){

  console.log("-------------Getting Server Info ------------");

  var client = redis.createClient({
    host: envconfig.redis.host,
    port: envconfig.redis.port,
    password: global.serverCache.get('masterPassword'),
  });

  client.on('error', function (err) {
    console.log("Error Fetching information from redis ---------------- " + err);
    errorCallback(err);
    client.quit();
  });

  client.on('ready', function () {
    console.log("On Ready");
    successCallback(client.server_info);
    client.quit();
  });

};


//Test
/*
exports.getServerInfo(function(response){
  console.log(response)
});
*/
