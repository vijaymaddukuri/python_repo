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
 * Created by mannam4 on 7/8/2016.
 */
var sql = require('mssql');

exports.testSQLConnectivity = function(server,port, database,user,password,successCallback,errorCallback){
  var config = {
    user: user,
    password: password,
    server: server,
    port: port,
    database: database
    /*options: {
     encrypt: true // Use this if you're on Windows Azure
     }*/
  };

  console.log("connecting");
  sql.connect(config).then(function() {
    // Query
    // Stored Procedure
    console.log("Success");
    successCallback();
    sql.close();

  }).catch(function(err) {
    // ... error checks
    console.error(err)
    errorCallback(err);

  });
};


exports.testSQLConnectivity('lglod153.lss.emc.com', '1433', 'vro', 'ehcdomain\\svc_vro','Password123!');
