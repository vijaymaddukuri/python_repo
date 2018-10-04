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

var appconfig = require('../../config/environment');

var config = require('../../config/environment');
var encryption = require('../../components/encrypt/encrypt');
var couchStore = require('../../components/dbConnect/couchdbConnect');
var db = couchStore.getCouchConnection(appconfig.couch.server,appconfig.couch.port,appconfig.couch.database);
const viewUrl = 'collections/project';

var decryptAllPasswords=function(inputData){

  var encryptionKey = null;

  if(inputData.components) {
    encryptionKey = inputData.components.encryptionKey;
  } else {
    console.error("No components found");
    return null;
  }
  encryption.decryptAllPasswordFields(inputData, encryptionKey);
  return this;
}

//couch changes

var create= function(project) {
  return new Promise(function(result,error){
    db.save(project, function (err, response) {
      if(response){
        result(response);
      }else if(err){
        error(error);
      }
    });
  });
}

var update= function(project) {
  return new Promise(function (result, error) {
    db.save(project, function (err, response) {
      if(response){
        result(response);
      }else if(err){
        error(error);
      }
    });
  });
}

// Deletes a Project from the DB
var remove = function(projectid) {
  return new Promise(function (result,error){
    db.remove(projectid, function(err, response){
      if(response){
        result(response);
      }else if(err){
        error(err);
      }
    });
  });
}

var find = function(req){
  return new Promise(function (result,error) {
    db.view(viewUrl,{include_docs:true},function (err,docs) {
      if(docs){
        var json=JSON.parse(docs);
        var valueJson=[];
        var request = JSON.parse(JSON.stringify(req));
        var reqField = Object.keys(request)[0];
        json.map(function (doc) {
          if(doc.value){
            if(doc.value[reqField] === request[reqField]) {
              valueJson.push(doc.value);
            }
          }
        });//end of map
        return result(valueJson);
      }else if(err){
        return error(err);
      }
    })//end of get
  });//end of promise
}

var findById = function(projectid) {
  console.log("Finding project by id " + projectid);
  return new Promise(function (result,error) {
    db.get(projectid, function (err, doc) {
      if(doc){
        return result(doc);
      }else if(err){
        return error(err);
      }
    });
  });
}

module.exports.decryptAllPasswords = decryptAllPasswords;
module.exports.find = find;
module.exports.findById = findById;
module.exports.remove = remove;
module.exports.update = update;
module.exports.create = create;
