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
 * GET     /api/kue              ->  index
 * POST    /api/kue              ->  create
 * GET     /api/kue/:id          ->  show
 * PUT     /api/kue/:id          ->  update
 * DELETE  /api/kue/:id          ->  destroy
 */

'use strict';

import _ from 'lodash';
import Kue from './kue.model';

var kueapi = require('../../components/kue/kueAPI').kueAPI();

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

// Gets a list of Kues
export function index(req, res) {
  /*return Kue.find().exec()
    .then(respondWithResult(res))
    .catch(handleError(res));*/

  return kueapi.getJobs(respondWithResult(res), handleError(res));

}

// Gets a single Kue from the DB
export function show(req, res) {
  /*return Kue.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(respondWithResult(res))
    .catch(handleError(res));*/

  return kueapi.getJob(req.params.id, respondWithResult(res), handleError(res));

}


// Kill a job and return job object
export function kill(req, res) {
  /*return Kue.findById(req.params.id).exec()
   .then(handleEntityNotFound(res))
   .then(respondWithResult(res))
   .catch(handleError(res));*/

  return kueapi.killJob(req.params.id, req.body.ansibleId, function(){
    kueapi.getJob(req.params.id, respondWithResult(res), handleError(res));

  }, handleError(res));

}

/*// Creates a new Kue in the DB
export function create(req, res) {
  return Kue.create(req.body)
    .then(respondWithResult(res, 201))
    .catch(handleError(res));
}*/


/*
// Deletes a Kue from the DB
export function destroy(req, res) {
  return Kue.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(removeEntity(res))
    .catch(handleError(res));
}
*/
