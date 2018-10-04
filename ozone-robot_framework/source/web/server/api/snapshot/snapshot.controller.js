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
 * GET     /api/snapshots              ->  index
 * POST    /api/snapshots              ->  create
 * GET     /api/snapshots/:id          ->  show
 * PUT     /api/snapshots/:id          ->  update
 * DELETE  /api/snapshots/:id          ->  destroy
 */

'use strict';

import _ from 'lodash';
import Snapshot from './snapshot.model';
var snaptool = require('../../components/snaptool/snaptool');

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
    var updated = _.merge(entity, updates);
    return updated.save()
      .then(updated => {
        return updated;
      });
  };
}

function removeEntity(res) {
  return function(entity) {
    if (entity) {
      return entity.remove()
        .then(() => {
          res.status(204).end();
        });
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
    return res.status(statusCode).send(err);
  };
}

// Gets a list of Snapshots
export function index(req, res) {
  var refid = req.query.refid;
  return Snapshot.find({user:req.user.ntid,refid:refid}).exec()
    .then(respondWithResult(res))
    .catch(handleError(res));
}


// Gets a single Snapshot from the DB
export function show(req, res) {
  return Snapshot.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(respondWithResult(res))
    .catch(handleError(res));
}

/**
 * Get Logs
 * @param req
 * @param res
 * @returns {*}
 */
export function getLogs(req, res) {
  return Snapshot.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(function(entity){
      if(!entity.jobId){
        return res.send("{ozone_display_item:{'type':'PROGRESS','message':'100'}}")
      }
      console.log("Logfile = " + entity.logfile);
      snaptool.getLogs(entity,
        function(successData){
          return res.send(successData);
        },
        function(errorData){
          console.log("Error " + errorData);
          return res.status(500).send(errorData)
        }
      );
      return null;
    })
    .catch(handleError(res));
}

// Creates a new Snapshot in the DB
export function create(req, res) {

  var snapshotData = req.body;
  var componentType = snapshotData.type;
  var time = new Date().getTime();
  var logfilename = 'snapshot_' + componentType + '_' + req.user.name.replace(" ","_") + '_' + time + '.log';

  //TODO: Only store part of user details
  var snapshotObject= {
    name: componentType,
    //info: snapshotData,
    info: {operation: snapshotData.operation},
    user: req.user.ntid,
    userInfo: req.user,
    type: componentType,
    operation: snapshotData.operation,
    logfile: logfilename,
    project: snapshotData.project._id,
    date: new Date(),
    refid: snapshotData.refid
  };

  Snapshot.create(snapshotObject)
    .then(function(entity) {
      if (entity) {
        try{

          snaptool.configure(entity, req.user.name,snapshotData,logfilename,
            function(data){
              entity.state = "active";
              entity.jobId = data.id;
              entity.save().then(entity => {
                return res.status(201).json(entity);
              })
            },
            function(error){
              entity.state = "Error";
              entity.errorData = error;
              entity.save().then(entity => {
                return res.status(500).json({error:entity.errorData});
              })
            }
          );
        }catch(e){
          console.log("Error " + e);
          return res.status(500).send(e);
        }

      }
    })
    .catch(handleError(res));

}


// List existing snapshots
export function listSnapshots(req, res) {

  var snapshotData = req.body;
  var componentType = snapshotData.type;
  //var time = new Date().getTime();
  var logfilename = 'snapshot_' + req.user.name.replace(" ","_") + '_.log';

  var responseSent = false;
  snaptool.configure(null, req.user.name,snapshotData,logfilename,
    function(data){
      //res.send(data)
      //Complete Callback
      if (!responseSent){
        console.log("Sending data complete")
        res.write(data);
        res.end()
        responseSent = true;
      }

    },
    function(error){
      if (!responseSent) {
        res.status(500).write(error);
      }

    });

}

// Updates an existing Snapshot in the DB
export function update(req, res) {
  if (req.body._id) {
    delete req.body._id;
  }
  return Snapshot.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(saveUpdates(req.body))
    .then(respondWithResult(res))
    .catch(handleError(res));
}

// Deletes a Snapshot from the DB
export function destroy(req, res) {
  return Snapshot.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(removeEntity(res))
    .catch(handleError(res));
}
