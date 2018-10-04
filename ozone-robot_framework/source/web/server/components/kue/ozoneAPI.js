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


'use strict';

var request = require('request');

var token_cache = {};

/**
 * @module
 * @name ozoneAPI
 * @description Module used to interact with Ozone API.
 * This module can be used by a third party to update Ozone Database such as KueProcessor/Ansible
 * @param {string} ozoneHost
 * @param {string} ozonePort
 * @param {string} ozoneUsername
 * @param {string} ozonePassword
 * @param {string} accessToken
 */
function ozoneAPI(ozoneHost, ozonePort, ozoneUsername, ozonePassword, accessToken){

  return{
    _ozoneHost : ozoneHost,
    _ozonePort : ozonePort,
    _ozoneUsername : ozoneUsername,
    _ozonePassword : ozonePassword,
    _accessToken : accessToken,
    _BaseURI: 'http://' + ozoneHost + ':' + ozonePort ,
    _uri : {
      'auth' : '/auth/local',
      'ansible' : '/api/ansible'
    },

    /**
     * Submit HTTP Request
     * @function
     * @param {string} type Type of request : GET, POST, PUT, DELETE
     * @param {string} url API URL without http://hostname:port
     * @param {successCallback} successCallback
     * @param {errorCallback} errorCallback
     * @param {object} [data] Data to send for POST, PUT operations
     * @param {object} [tryLogin] Try to login if auth error
     */
    submitHttpRequest :  function(type, url, successCallback,errorCallback, data, tryLogin){
      const uri =  this._BaseURI + url;
      this.submitHttpRequestURI(type, uri, successCallback,errorCallback, data, tryLogin);
    },

    /**
     * Success callback
     * @callback successCallback
     */

    /**
     * Error callback
     * @callback errorCallback
     */

    /**
     * Submit HTTP Request URI
     * @function
     * @param {string} type Type of request : GET, POST, PUT, DELETE
     * @param {string} uri API URI with http://hostname:port
     * @param {successCallback} successCallback
     * @param {errorCallback} errorCallback
     * @param {object} data Data to post
     * @param {boolean} [tryLogin=true] Retry to login on Authentication failure
     */
    submitHttpRequestURI : function(type, uri, successCallback,errorCallback, data, tryLogin){
      //Set re try login to True by default. Unless it is explicitly set to false.
      if(typeof tryLogin === "undefined" || tryLogin === null)tryLogin = true;

      console.log("TryLogin=" + tryLogin);

      var THIS = this;
      request(
        {
          url : uri,
          method: type,
          headers : {
            "Content-Type" : 'application/json',
            "authorization" : 'Bearer ' + THIS._accessToken
          },
          rejectUnauthorized:false,
          json: data
        },
        function (error, response, body) {

          //If authorization fails try to login once
          if(response && response.statusCode === 401){

            console.log("401 Error and TryLogin=" + tryLogin);

            if(tryLogin){
              return THIS.reLogin(function(){
                THIS.submitHttpRequestURI(type, uri, successCallback, errorCallback, data, false)
              }, errorCallback)
            }
          }

          if(error || (response && response.statusCode >= 400)){
            console.log("OzoneAPI - Error submitting HTTP request");
            errorCallback(response, error);
          }else{
            console.log("OzoneAPI - Success submitting HTTP request");
            successCallback(response, body);
          }
        });
    },

    /**
     * Get KueAPI Statistics
     * @function
     * @param {string} username Ozone API Username
     * @param {string} password Ozone API Password
     * @param {successCallback} successCallback
     * @param {errorCallback} errorCallback
     */
    login: function(username, password, successCallback, errorCallback){

      this._ozoneUsername = username;
      this._ozonePassword = password;

      var authPayload = {
        'email': username,
        'password': password
      };

      let THIS = this;
      this.submitHttpRequest('POST',THIS._uri.auth,function(response, body){
        THIS._accessToken = body.token;
        successCallback(body.token);
      }, errorCallback, authPayload, false);


    },

    /**
     * Re Login using available credentials
     * @param {successCallback} successCallback
     * @param {successCallback} errorCallback
     */
    reLogin: function(successCallback, errorCallback){
      let THIS = this;

      //console.log("Username = " + this._ozoneUsername)
      //console.log("Password = " + this._ozonePassword)

      this.login(this._ozoneUsername, this._ozonePassword, function(token){
        THIS._accessToken = token;
        successCallback()
      }, errorCallback);

    },

    /**
     * Get list of all ansible Jobs
     * @function
     * @param {successCallback} successCallback
     * @param {errorCallback} errorCallback
     */
    getAnsibleJobs: function(successCallback, errorCallback){
      var THIS = this;
      this.submitHttpRequest('GET',THIS._uri.ansible,function(response, body){
        successCallback(body);

      }, errorCallback);

    },

    /**
     * Get Ansible Job Data
     * @function
     * @param ansibleId
     * @param {successCallback} successCallback
     * @param {errorCallback} errorCallback
     */
    getAnsibleJob: function(ansibleId, successCallback, errorCallback){
      console.log("Get Ansible Job =" + ansibleId);

      this.submitHttpRequest('GET',this._uri.ansible + '/' + ansibleId,function(response, body){
        console.log("Got Ansible Job =" + ansibleId);
        successCallback(body);
      }, errorCallback);

    },

    /**
     * Update Ansible Job
     * @param {string} ansibleId
     * @param {object} ansibleData
     * @param {successCallback} successCallback
     * @param {errorCallback} errorCallback
     */
    updateAnsibleJob: function(ansibleId, ansibleData, successCallback, errorCallback){
      var THIS = this;
      console.log("Update Ansible Job =" + ansibleId);
      this.submitHttpRequest('PUT', this._uri.ansible + '/' + ansibleId, function(response){
        console.log("Updated Ansible Job =" + ansibleId);
        successCallback(response, THIS._accessToken);
      }, errorCallback, ansibleData)

    },

    /**
     * Update Ansible Job Results
     * @param {string} ansibleId
     * @param {string} ansibleState
     * @param {object} ansibleResults
     * @param {string} ansibleStats
     * @param {successCallback} successCallback
     * @param {errorCallback} errorCallback
     */
    updateAnsibleJobResults: function(ansibleId, ansibleState, ansibleResults, ansibleStats, successCallback, errorCallback){
      var THIS = this;


      this.getAnsibleJob(ansibleId, function(ansibleObject){

        ansibleObject.ansibleState = ansibleState;
        ansibleObject.ansibleResults = ansibleResults;
        ansibleObject.ansibleStats = ansibleStats;

        THIS.updateAnsibleJob(ansibleId, ansibleObject, successCallback, errorCallback);

      }, errorCallback);
    },

  }

}


exports.ozoneAPI = ozoneAPI;

/**
 * Tests
 */
/*var ozoneAPI = ozoneAPI('10.247.69.95','9000');

ozoneAPI.login('admin@ozone.com','ozone',function(response){
  ozoneAPI.updateAnsibleJob("5811900de34fae3f1277ed50", {ansibleState:"Testing2"}, function(response){
    console.log(response)
  }, function(response){
    console.log(response)
  })

  /!*ozoneAPI.getAnsibleJob("5811900de34fae3f1277ed50",function(response){
    console.log(response);

  }, function(error, body){
    console.log("error" + error + body)
  })*!/

}, function(error, body){
  console.log("error" + error + body)
})*/

/*
kueapi.runJob({
    type:'exec',
    data:{
      "command": "/tmp/infiniteScript.sh"
    }
  },function(response){
    console.log(response)
  },function(response){
    console.log(response)
});
*/


/*
kueapi.getJobLogs(10,function(response){
  console.log(response)
},function(response){
  console.log(response)
});
*/


/*
kueapi.getJob(149, function(response){
  console.log(response)
});
*/

 // kueapi.killJob(237, function(response){
 //   console.log(response)
 // }, function(response){
 //   console.log(response)
 // });

