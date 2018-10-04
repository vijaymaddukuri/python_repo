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
 * @name kueAPI
 * @description Module used to interact with NodeJS Kue. Kue is a job queue processor. This module is used to get list of jobs
 * create new jobs, query job logs.
 */

var request = require('request');
var config =  require('../../config/environment');

const kueHost = config.kue.host;
const kuePort = config.kue.port;
var kueTerminalStates = ['failed','complete'];

function kueAPI(){

  return{
    _kueHost : kueHost,
    _kuePort : kuePort,
    _BaseURI: 'http://' + kueHost + ':' + kuePort ,
    _uri : {
      'stats' : '/stats',
      'job' : '/job'
    },
    kueTerminalStates: kueTerminalStates,

    /**
     * Submit HTTP Request
     * @function
     * @param {string} type Type of request : GET, POST, PUT, DELETE
     * @param {string} url API URL without http://hostname:port
     * @param {method} successCallback
     * @param {method} errorCallback
     * @param {object} data Data to post
     */
    submitHTTPrequest :  function(type, url, successCallback,errorCallback, data){
      var uri =  this._BaseURI + url;
      this.submitHTTPrequestURI(type, uri, successCallback,errorCallback, data);
    },

    /**
     * Submit HTTP Request URI
     * @function
     * @param {string} type Type of request : GET, POST, PUT, DELETE
     * @param {string} uri API URI with http://hostname:port
     * @param {method} successCallback
     * @param {method} errorCallback
     * @param {object} data Data to post
     */
    submitHTTPrequestURI : function(type, uri, successCallback,errorCallback, data){
      request(
        {
          url : uri,
          method: type,
          headers : {
            "Content-Type" : 'application/json'
          },
          rejectUnauthorized:false,
          json: data
        },
        function (error, response, body) {
          if(error){
            errorCallback(response, error);
          }else{
            successCallback(response, body);
          }
        });
    },

    /**
     * Get KueAPI Statistics
     * @function
     * @param {callback} successCallback
     * @param {callback} errorCallback
     */
    getStats: function(successCallback, errorCallback){

      var THIS = this;
      this.submitHTTPrequest('GET',THIS._uri.stats,function(response, body){
        var results = JSON.parse(body);
        successCallback(results);

      }, errorCallback);

    },
    /**
     * Get list of all Jobs
     * @function
     * @param {callback} successCallback
     * @param {callback} errorCallback
     */
    getJobs: function(successCallback, errorCallback){
      var THIS = this;
      this.submitHTTPrequest('GET',THIS._uri.job,function(response, body){
        var results = JSON.parse(body);
        successCallback(results);

      }, errorCallback);

    },
    /**
     * Get Job
     * @function
     * @param {string} jobId Job ID as displayed in Kue Web
     * @param {callback} successCallback
     * @param {callback} errorCallback
     */
    getJob: function(jobId, successCallback, errorCallback){
      var THIS = this;
      this.submitHTTPrequest('GET',THIS._uri.job + '/' + jobId,function(response, body){
        var results = JSON.parse(body);
        successCallback(results);

      }, errorCallback);

    },

    /**
     * Get Job Logs
     * @function
     * @param {string} jobId
     * @param {callback} successCallback
     * @param {callback} errorCallback
     */
    getJobLogs: function(jobId, successCallback, errorCallback){
      var THIS = this;
      this.submitHTTPrequest('GET',THIS._uri.job + '/' + jobId + '/log',function(response, body){
        var results = JSON.parse(body);
        successCallback(results);

      }, errorCallback);

    },

    /**
     * Run Job
     * @function
     * @param {string} jobData
     * @param {string} successCallback
     * @param {string} errorCallback
     */
    runJob: function(jobData, successCallback, errorCallback){
      var THIS = this;
      this.submitHTTPrequest('POST',THIS._uri.job,function(response, body){
        var results = body;
        successCallback(results);
      }, errorCallback, jobData);

    },

    /**
     * Stop a running Job by sending stop message to Redis Pub/Sub. Each job run by kue and ansible call back plugin subscribes to Redis Pub/Sub module 'stop' message.
     * On receiving 'stop' message the Ansible strategy plugin skips all remaining tasks.
     * The job is not immediately terminated by this
     * @param {string} jobId
     * @param {string} ansibleId
     * @param {callback} successCallback
     * @param {callback} errorCallback
     */
    stopJob: function(jobId, ansibleId, successCallback, errorCallback){
      var THIS = this;

      var pubSub = require('../messaging/pubSub').pubSub();
      console.log("Sending stop message to " + jobId + " " + ansibleId);
      pubSub.emit('stop', { jobid:jobId, ansibleId:ansibleId}, successCallback, errorCallback, 'kue');

    },

    /**
     * Kill a running Job by sending kill message to Redis Pub/Sub. Each job run by kue subscribes to Redis Pub/Sub module 'kill' message.
     * On receiving 'kill' message the job tree is killed. All processes in the process tree initiated by the job are killed.
     * @param jobId
     * @param ansibleId
     * @param successCallback
     * @param errorCallback
     */
    killJob: function(jobId, ansibleId, successCallback, errorCallback){
      var THIS = this;

      var pubSub = require('../messaging/pubSub').pubSub();
      console.log("Sending kill message to " + jobId + " " + ansibleId);
      pubSub.emit('kill', { jobid:jobId, ansibleId:ansibleId}, successCallback, errorCallback, 'kue');

    },

    /**
     * Delete Job
     * @param jobID
     * @param successCallback
     * @param errorCallback
     */
    deleteJob: function(jobID, successCallback, errorCallback){

      var THIS = this;
      var delete_uri = THIS._uri.job + "/" + jobID;
      this.submitHTTPrequest('DELETE',delete_uri,function(response, body){
        var results = body;
        successCallback(results);
      }, errorCallback);

    }

  }

}


exports.kueAPI = kueAPI;

