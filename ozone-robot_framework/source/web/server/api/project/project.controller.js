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
 * Using Rails-like standard naming convention for endpoints.
 * GET     /api/projects              ->  index
 * POST    /api/projects              ->  create
 * GET     /api/projects/:id          ->  show
 * PUT     /api/projects/:id          ->  update
 * DELETE  /api/projects/:id          ->  destroy
 */

'use strict';

import _ from 'lodash';
import Project from './project.model';
var dbUtil = require('../../components/utils/dbutility');
var emailer = require('../../components/email/email_smtp.js');
var config = require('../../config/environment');
var ansible = require('../../components/ansibletool/ansibletool');
var encryption = require('../../components/encrypt/encrypt');

// config.serverCache.get('password');

function respondWithResult(res, statusCode) {
  statusCode = statusCode || 200;
  return function(entity) {
    if (entity) {
      return res.status(statusCode).json(entity);
    }
  };
}

function saveUpdates(updates) {
  return function(entity) {
    //var updated = _.merge(entity, updates);
    var updated = dbUtil.updateDocument(entity,Project,updates);

    var encryptionKey = encryption.encryptAllPasswordFields(updated);
    if(updated.components)
      updated.components.encryptionKey = encryptionKey;

    return Project.update(updated)
        .then( (result) => {
        console.log('returning result --> ' + result);
    return result;
  });
  };
}

function removeEntity(res) {
  return function(entity) {
    if (entity) {
      console.log('entity --> ' + entity);
      return res.status(204).json(entity);
    }
  };
}

function handleEntityNotFound(res) {
  return function(entity) {
    if (!entity) {
      res.status(404).end();
      return null;
    }
    return entity;
  };
}

function handleError(res, statusCode) {
  statusCode = statusCode || 500;
  return function(err) {
    res.status(statusCode).send(err);
  };
}

// Gets a list of Projects
export function index(req, res) {

  var filter = null;

  //if(req.user.name !== "Admin"){
    filter = {user:req.user._id};
  //}

  // Database operation
  return Project.find(filter)
    .then(respondWithResult(res))
    .catch(handleError(res));
}

// Gets a single Project from the DB
export function show(req, res) {
  return Project.findById(req.params.id)
    .then(handleEntityNotFound(res))
    .then(respondWithResult(res))
    .catch(handleError(res));
}

// Creates a new Project in the DB
export function create(req, res) {
  req.body.user = req.user._id;
  req.body.components = config.defaults[req.body.type];
  req.body.doc_type = 'project';

  // Check if a project folder by the same name already exists.
  // If so fail project creation

  var projectFolder = config.scriptEngine.projectsFolder + req.body.name;

  ansible.checkIfFolderExists(req.body.user, projectFolder, function(){

    // Send error message.
    res.status(500).send("A project with the same name already exists. Please try a different name");

  }, function(){

    // Try creating an empty folder.
    ansible.createFolder(req.body.user, projectFolder, function(){
      // If folder creation is success create project
      return Project.create(req.body)
        .then(respondWithResult(res, 201))
        .catch(handleError(res));
    }, function(errorResponse){
      // If folder creation fails, fail project creation
      res.status(500).send(errorResponse);
    })

  });


}

export function getDefaultConfigData(req, res){
  res.send(config.defaults)
}


export function getDecryptedData(req, res){
  return Project.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(function(entity){
      return res.send(Project.decryptAllPasswords(entity));
    })
    .catch(handleError(res));
}

// Updates an existing Project in the DB
export function update(req, res) {
  if (req.body._id) {
    delete req.body._id;
  }
  req.body.user = req.user._id;

  return Project.findById(req.params.id)
    .then(handleEntityNotFound(res))
    .then(saveUpdates(req.body))
    .then(respondWithResult(res))
    .catch(handleError(res));
}

export function updateAnsibleVariableFiles(req, res){

  var project = req.body;
  ansible.updateAnsibleVariableFiles(req.user, project,function(response){
      res.send(response);
    },
    function(response){
      res.status(500).send(response);
    });

}

/**
 * Update Ansible Playbook Files and roles from the template directory
 * @param {Object} req API Request
 * @param {Object} res API Response
 */
export function updateAnsiblePlaybookFiles(req, res){

  var project = req.body;
  ansible.copyAnsibleProjectTemplate(req.user, project.name, function(){

    },function(response){
      res.send(response);
    },
    function(response){
      res.status(500).send(response);
    });

}



export function downloadInputTemplate(req, res){
  res.download('client/assets/downloads/Ozone _Input_Template_v0.1.xlsx');
}

// Deletes a Project from the DB
export function destroy(req, res) {

  return Project.findById(req.params.id)
    .then(handleEntityNotFound(res))
    .then(function(project) {
      console.log("Found project " + project._id);
      // Delete project folder from filesystem
      ansible.deleteProjectFolder(req.user,project.name,function(){
        return Project.remove(req.params.id)
          .then(removeEntity(res))
          .catch(handleError(res));
      }, function(err){
          res.status(500).send(err);
      })

    })
    .catch(handleError(res));

}
