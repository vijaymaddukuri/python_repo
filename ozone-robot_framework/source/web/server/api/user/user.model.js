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

import crypto from 'crypto';
import appconfig from '../../config/environment';

var jwt = require('jsonwebtoken');
var config = require('../../config/environment');
var encryption = require('../../components/encrypt/encrypt');
var couchStore = require('../../components/dbConnect/couchdbConnect');
var db = couchStore.getCouchConnection(appconfig.couch.server,appconfig.couch.port,appconfig.couch.database);
const viewUrl = 'collections/user';


/**
 * Authenticate - check if the passwords are the same
 *
 * @param {String} password
 * @param {Function} callback
 * @return {Boolean}
 * @api public
 */
var authenticate = function(password, encryptedpassword,salt, callback) {
  if (!callback) {
    return password === encryptPassword(password,salt);
  }

  encryptPassword(password, salt, (err, pwdGen) => {
    if (err) {
      return callback(err);
    }
    if (encryptedpassword === pwdGen) {
      callback(null, true);
    } else {
      callback(null, false);
    }
  });
}

/**
 * Encrypt password
 *
 * @param {String} password
 * @param {Function} callback
 * @return {String}
 * @api public
 */
function encryptPassword(password, saltgenerated, callback) {
  if (!password || !saltgenerated) {
    if (!callback) {
      return null;
    } else {
      return callback('Missing password or salt');
    }
  }

  var defaultIterations = 10000;
  var defaultKeyLength = 64;
  var salt = new Buffer(saltgenerated, 'base64');

  if (!callback) {
    return crypto.pbkdf2Sync(password, salt, defaultIterations, defaultKeyLength)
      .toString('base64');
  }

  return crypto.pbkdf2(password, salt, defaultIterations, defaultKeyLength, (err, key) => {
      if (err) {
        callback(err);
      } else {
        callback(null, key.toString('base64'));
}
});
}

var findone = function(req,removeSaltAndPassword){
  return new Promise(function (result,error) {
    db.view(viewUrl,{include_docs:true}, function (err, docs) {
      if(docs){
        var json = JSON.parse(docs);
        var valueJson=[];
        var request = JSON.parse(JSON.stringify(req));
        var reqField = Object.keys(request)[0];
        json.map(function(doc){
          if(doc.value){
            if(doc.value[reqField] === request[reqField]){
              if (removeSaltAndPassword) {
                delete doc.value["salt"];
                delete doc.value["password"];
              }
              valueJson.push(doc.value);
            }
          }
        });
        return result(valueJson);
      }else if(err){
        console.log('got error from couch. reason : ' + err);
        return error(err);
      }
    });//end of view method
  });//end of promise
};

var find = function(req,removeSaltAndPassword){
  return new Promise(function (result,error) {
    db.view(viewUrl,{include_docs:true}, function (err, docs) {
      if(docs){
        var json = JSON.parse(docs);
        var valueJson=[];
        var request = JSON.parse(JSON.stringify(req));
        var reqField = Object.keys(request)[0];
        json.map(function(doc){
          if(doc.value){
            if (removeSaltAndPassword) {
              delete doc.value["salt"];
              delete doc.value["password"];
            }
            valueJson.push(doc.value);
          }
        });
        return result(valueJson);
      }else if(err){
        console.log('got error from couch. reason : ' + err);
        return error(err);
      }
    });//end of view method
  });//end of promise
};

var findById = function(userId){
  return new Promise(function (result,error) {
    db.get(userId, function (err, doc) {
      if(doc){
        delete doc["salt"];
        delete doc["password"];
        return result(doc);
      }else if(err){
        return error(err);
      }
    });
  });//end of promise
};

var create = function(user){
  var userDoc = JSON.parse(JSON.stringify(user));
  return new Promise(function(result,error){
    userDoc.doc_type = 'user';
    validateAndEncrypt(userDoc, function(encrypted,err){
      if(encrypted){
        saveorupdate(userDoc)
          .then((token) => result(token))
      .catch((saveError) => error(saveError));
      }
      if(err){
        res.send('error occured : Reason ' + err);
      }
    });
  });
};

function validateAndEncrypt(doc, callback){

  // Make salt with a callback
  makeSalt((saltErr, salt) => {
    if (saltErr) {
      console.log('salt error' + saltErr);
      callback(null,saltErr);
    }
    //setting salt to the document
    if(salt){
      doc.salt = salt;
      encryptPassword(doc.password, salt,(encryptErr, hashedPassword) => {
        if (encryptErr) {
          callback(null,encryptErr);
        }
        if(hashedPassword){
          doc.password = hashedPassword;
          callback('password encrypted',null);
        }
      });
    }
  });
}

/**
 * Make salt
 *
 * @param {Number} byteSize Optional salt byte size, default to 16
 * @param {Function} callback
 * @return {String}
 * @api public
 */
function makeSalt(byteSize, callback) {
  var defaultByteSize = 16;
  if (typeof arguments[0] === 'function') {
    callback = arguments[0];
    byteSize = defaultByteSize;
  } else if (typeof arguments[1] === 'function') {
    callback = arguments[1];
  }

  if (!byteSize) {
    byteSize = defaultByteSize;
  }

  if (!callback) {
    return crypto.randomBytes(byteSize).toString('base64');
  }

  return crypto.randomBytes(byteSize, (err, salt) => {
      if (err) {
        callback(err);
      } else {
        callback(null, salt.toString('base64'));
}
});
}

function saveorupdate(doc){
  return new Promise(function(result,error){
    db.save(doc, function (err, response) {
      if(response){
        var token = jwt.sign({ _id: result.id }, config.secrets.session, {
          expiresIn: 60 * 60 * 5
        });
        //res.json({ token });
        result(token);
      }else if(err){
        //res.send('error occured while saving the document. Reason : ' + err);
        error(err);
      }
    });
  });

};


module.exports.findone = findone;
module.exports.authenticate = authenticate;
module.exports.findById = findById;
module.exports.create = create;
module.exports.saveorupdate = saveorupdate;
module.exports.find = find;
