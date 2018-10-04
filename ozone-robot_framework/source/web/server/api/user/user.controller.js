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

import User from './user.model';
import passport from 'passport';
import config from '../../config/environment';
import jwt from 'jsonwebtoken';
import _ from 'lodash';

var emailer = require('../../components/email/email_smtp.js');

function validationError(res, statusCode) {
  statusCode = statusCode || 422;
  return function (err) {
    res.status(statusCode).json(err);
  }
}

function respondWithResult(res, statusCode) {
  statusCode = statusCode || 200;
  return function (entity) {
    if (entity) {
      return res.status(statusCode).json(entity);
    }
  };
}


function saveUpdates(updates) {
  return function (entity) {
    var updated = _.merge(entity, updates);
    return updated.save()
      .then(updated => {
        return updated;
      });
  };
}

function handleEntityNotFound(res) {
  return function (entity) {
    if (!entity) {
      res.status(404).end();
      return null;
    }
    return entity;
  };
}

function handleError(res, statusCode) {
  statusCode = statusCode || 500;
  return function (err) {
    res.status(statusCode).send(err);
  };
}

/**
 * Get list of users
 * restriction: 'admin'
 */
export function index(req, res) {
  return User.find({}, '-salt -password')
    .then(users => {
      res.status(200).json(users);
    })
    .catch(handleError(res));
}

/**
 * Creates a new user
 */
export function create(req, res, next) {
  /*var newUser = new User(req.body);
   newUser.provider = 'local';
   newUser.role = 'user';

   newUser.save()
   .then(function(user) {
   var token = jwt.sign({ _id: user._id }, config.secrets.session, {
   expiresIn: 60 * 60 * 5
   });
   res.json({ token });
   })
   .catch(validationError(res));*/

  User.create(req.body)
    .then(token => {
      if (token) {
        res.json({token});
      }
    })
    .catch(validationError(res));
}

/**
 * Get a single user
 */
export function show(req, res, next) {
  var userId = req.params.id;

  return User.findById(userId).exec()
    .then(user => {
      if (!user) {
        return res.status(404).end();
      }
      res.json(user.profile);
    })
    .catch(err => next(err));
}


/**
 * Deletes a user
 * restriction: 'admin'
 */
export function destroy(req, res) {
  return User.findByIdAndRemove(req.params.id).exec()
    .then(function () {
      res.status(204).end();
    })
    .catch(handleError(res));
}

/**
 * Change a users password
 */
export function changePassword(req, res, next) {
  var userId = req.user._id;
  var oldPass = String(req.body.oldPassword);
  var newPass = String(req.body.newPassword);

  return User.findById(userId)
    .then(user => {
      // if (user.authenticate(oldPass)) {
        user.password = newPass;
        //return user.save()
      return User.create(user)
          .then(() => {
            res.status(204).end();
          })
          .catch(validationError(res));
      // } else {
      //   return res.status(403).end();
      // }
    });
}

// Updates an existing Deploy in the DB
export function update(req, res) {
  if (req.body._id) {
    delete req.body._id;
  }
  return User.findById(req.params.id).exec()
    .then(handleEntityNotFound(res))
    .then(saveUpdates(req.body))
    .then(respondWithResult(res))
    .catch(handleError(res));
}

/**
 * Get my info
 */
export function me(req, res, next) {
  //is Username
  var userId = req.user._id;

  return User.findById(userId)
    .then(user => { // don't ever give out the password or salt
      if (!user) {
        console.log('returning 401 from user controller');
        return res.status(401).end();
      }
      return res.json(user);
    }).catch(err => next(err));
}

/**
 * Authentication callback
 */
export function authCallback(req, res, next) {
  res.redirect('/');
}


export function email(req, res) {

  console.log("Req user ntid =" + req.user.ntid);

}


export function ehcDefaultUsers(req, res) {
  var Converter = require("csvtojson").Converter;
  var converter = new Converter({});

//end_parsed will be emitted once parsing finished
  converter.on("end_parsed", function (jsonArray) {
    //console.log(jsonArray); //here is your result jsonarray
    res.send(jsonArray)
  });

  require('fs').createReadStream('server/config/EHCUsers.csv').pipe(converter)
}

