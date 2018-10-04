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


var crypto = require('crypto');


var algorithm = 'aes-256-ctr';

var Encryption = function(){

  this.encryptionKey = makeSalt(64);

  this.isArray = function(o) {
    return Object.prototype.toString.call(o) === '[object Array]';
  };

  this.traverseArray = function(arr) {
    var THIS = this;
    arr.forEach(function(x) {
      THIS.traverse(x);
    });
  };

  this.traverseObject = function(obj) {
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        this.traverse(obj[key], obj, key);
      }
    }
  };

  this.traverse = function (x, parent,key) {
    if (this.isArray(x)) {
      this.traverseArray(x);
    } else if ((typeof x === 'object') && (x !== null)) {
      this.traverseObject(x);
    } else {
      if(parent && (key.indexOf('password') > -1 || key.indexOf('passphrase') > -1)){
        if(!this.decrypt){
          parent[key] = encrypt(parent[key], this.encryptionKey)
        }else{
          parent[key] = exports.decrypt(parent[key], this.encryptionKey)
        }
      }
    }
  };

  this.decryptAll = function (inputData, encryptionKey) {
    this.decrypt = true;
    this.encryptionKey = encryptionKey;
    this.traverse(inputData);
  };

  this.encryptAll = function (inputData) {
    this.decrypt = false;
    this.traverse(inputData);
  };

};

/**
 * Make encryptionKey
 *
 * @param {Number} byteSize Optional encryptionKey byte size, default to 16
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

  return crypto.randomBytes(byteSize, (err, encryptionKey) => {
    if (err) {
      callback(err);
    } else {
      callback(null, encryptionKey.toString('base64'));
    }
  });
}



function encrypt(password,encryptionKey){
  var cipher = crypto.createCipher(algorithm,encryptionKey);
  var crypted = cipher.update(password,'utf8','base64');
  crypted += cipher.final('base64');
  return crypted;
}

exports.decrypt = function(password,encryptionKey){
  var decipher = crypto.createDecipher(algorithm,encryptionKey);
  var dec = decipher.update(password,'base64','utf8');
  dec += decipher.final('utf8');
  return dec;
};

/**
 * Encrypt all passwords in an object
 * @param {Object} inputData Json object
 * @returns {String} Salt - Returns encryptionKey that can be used to decrypt passwords
 */
exports.encryptAllPasswordFields = function(inputData){
  //var encryptionKey = makeSalt(64);

  var enc = new Encryption();
  enc.encryptAll(inputData);
  return enc.encryptionKey;
};

/**
 * Decrypt All passwords in an object
 * @param inputData
 * @param salt
 */
exports.decryptAllPasswordFields = function(inputData, encryptionKey){
  var enc = new Encryption();
  enc.decryptAll(inputData, encryptionKey);
};


/* Test */
/*

var inputData = {
  "_id": "57d9870206dbe38008e03d13",
  "capacityType": "GB",
  "components": {
    "import_data": {
      "vars": {
        "vrealize_orchestrator": {
          "vro_configurator_username": "vmware",
          "vro_configurator_password": "VMwar3!!",
          "vipr_workflow_timeout_minutes": "30",
          "local_qsvro_p12_keystore_path": "D:\\\\ehc35_certs\\\\vRO-quali\\\\qsvro.p12"
        },
        "common": {
          "local_vipr_ova_path": "/ehc4_repo/ViPR/vipr-3.0.0.1.38/vipr-3.0.0.1.38-controller-2+1.ova",
          "ehc_ou": "EHC",
          "adbind_logi_username": "adbind_logi",
          "adbind_logi_password": "Password123!",
          "adbind_sso_username": "adbind_sso",
          "adbind_sso_passphrase": "Password123!",
          "adbind_vro_username": "adbind_vro",
          "adbind_vro_password": "Password123!",
          "adbind_vipr_username": "adbind_vipr",
          "svc_sqlsvragent_username": "svc_sqlsvragent",
          "ehc_backup_services_group_name": "EHC_Backup_Services",
          "ehc_fabric_admins_group_name": "EHC_Fabric_Admins",
        }
      }
    }
  }
};


var encryptionKey = exports.encryptAllPasswordFields(inputData);

console.log(JSON.stringify(inputData, null, '\t'));

exports.decryptAllPasswordFields(inputData,encryptionKey);

console.log(JSON.stringify(inputData, null, '\t'));
*/
