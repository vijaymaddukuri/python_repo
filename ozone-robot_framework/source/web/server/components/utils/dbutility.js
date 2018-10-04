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


var _ = require('underscore');

exports.updateDocument = function(doc, SchemaTarget, data) {
  var reqFields = Object.keys(data);

  for (var i=0; i < reqFields.length;i++) {
    var field =reqFields[i];
    if ((field !== '_id') && (field !== '_rev')) {
      var newValue = getObjValue(field, data);
      if (newValue !== undefined) {
        setObjValue(field, doc, newValue);
      }
    }
  }
  return doc;
};



function getObjValue(field, data) {
  return _.reduce(field.split("."), function(obj, f) {
    if(obj) return obj[f];
  }, data);
}

function setObjValue(field, data, value) {
  var fieldArr = field.split('.');
  return _.reduce(fieldArr, function(o, f, i) {
    if(i == fieldArr.length-1) {
      o[f] = value;
    } else {
      if(!o[f]) o[f] = {};
    }
    return o[f];
  }, data);
}
