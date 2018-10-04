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
 * GET     /api/upgrade              ->  index
 * POST    /api/upgrade              ->  create
 * GET     /api/upgrade/:id          ->  show
 * PUT     /api/upgrade/:id          ->  update
 * DELETE  /api/upgrade/:id          ->  destroy
 */

'use strict';

import _ from 'lodash';
import Upgrade from './upgrade.model';
var upgradetool = require('../../components/upgrade/upgradetool');

function respondWithResult(res, statusCode) {
  statusCode = statusCode || 200;
  return function(entity) {
    if (entity) {
      res.status(statusCode).json(entity);
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
    res.status(statusCode).send(err);
  };
}

// Gets a list of Upgrades
export function index(req, res) {
  return Upgrade.find().exec()
    .then(respondWithResult(res))
    .catch(handleError(res));
}

// Gets a single Upgrade from the DB
export function show(req, res) {
  return Upgrade.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(respondWithResult(res))
    .catch(handleError(res));
}


export function getLogs(req, res) {
  return Upgrade.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(function(entity){
      upgradetool.getLogs(entity.logfile,
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

// Creates a new Upgrade in the DB
/*
export function create(req, res) {
  return Upgrade.create(req.body)
    .then(respondWithResult(res, 201))
    .catch(handleError(res));
}
*/

export function create(req, res) {

  var time = new Date().getTime();
  var logfilename = req.user.name + '_' + time + '.log';

  var upgradeObject= {
    name: 'Upgrade',
    info: '',
    user: req.user.name,
    date: time,
    logfile: logfilename
  };

  var createdEntity = null;

  upgradetool.upgrade(req.user.name,upgradeObject,logfilename,
    function(data){
      //res.send(data)

    },
    function(data){
      //res.send(data)

    },
    function(error){
      //res.status(500).send(error);
    }
  );

  return Upgrade.create(upgradeObject)
    .then(function(entity) {
      if (entity) {
        createdEntity = entity;
        return res.status(201).json(entity);
      }
    })
    .catch(handleError(res));

}


export function checkUpdates(req, res) {

  var responseEnded = false;
  upgradetool.checkUpdates(req.user.name,
    function(data){
      console.log("Data Call back");
      // if(!responseEnded)
      // res.write(data)
    },
    function(data){
      console.log("Complete Call back");
      if(!responseEnded){
        res.write(data);
        res.end();
        responseEnded = true
      }

    },
    function(error){
      console.log("Error Call back");
      if(!responseEnded){
        res.status(500).write(error);
        //res.end();
        //responseEnded = true
      }
    }
  );

}

// Updates an existing Upgrade in the DB
export function update(req, res) {
  if (req.body._id) {
    delete req.body._id;
  }
  return Upgrade.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(saveUpdates(req.body))
    .then(respondWithResult(res))
    .catch(handleError(res));
}

// Deletes a Upgrade from the DB
export function destroy(req, res) {
  return Upgrade.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(removeEntity(res))
    .catch(handleError(res));
}
