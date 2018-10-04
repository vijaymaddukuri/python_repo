'use strict';

var appconfig = require('../../config/environment');

var config = require('../../config/environment');
var encryption = require('../../components/encrypt/encrypt');
var couchStore = require('../../components/dbConnect/couchdbConnect');
// DB Connection used for all database operation
var db = couchStore.getCouchConnection(appconfig.couch.server,appconfig.couch.port,appconfig.couch.database);
// Raw connection used to get total rows count. Above connection doesn't provide easy way for that.
var db_raw_connection = couchStore.getCouchConnection(appconfig.couch.server,appconfig.couch.port,appconfig.couch.database,true);
const viewUrl = 'collections/ansible';

var create= function(config) {
  return new Promise(function(result,error){
    db.save(config, function (err, response) {
      if(response){
        result(response);
      }else if(err){
        error(error);
      }
    });
  });
};

var findById = function(configid) {
  return new Promise(function (result,error) {
    db.get(configid, function (err, doc) {
      if(doc){
        return result(doc);
      }else if(err){
        return error(err);
      }
    });
  });
};

function find_in_object(my_object, my_criteria){

  return my_object.filter(function(obj) {
    return Object.keys(my_criteria).every(function(c) {
      return obj.value[c] == my_criteria[c];
    });
  });

}

/**
 * Exclude Keys
 * @param keys
 * @returns {Function}
 */
function exlcude_keys(keys){

  return function(doc){
    Object.keys(doc).map(function(c){
      if(keys.indexOf(c) > -1){
        delete doc[c];
      }
    });
    return doc
  }
}

/**
 * Get Total Rows in View
 * @param successCallback
 * @param errorCallback
 */
var getTotalRows = function(successCallback, errorCallback) {
  db_raw_connection.view(viewUrl, {limit: 0}, function (err, docs) {
    if(err)return errorCallback(err)
    successCallback(docs.total_rows)
  })
}

/**
 * Find ansible jobs by criteria and limit and sort by creation time
 * @param criteria
 * @param exclude_keys
 * @param limit
 * @param skip
 * @returns {Promise}
 */
var find = function(criteria, exclude_keys, limit, skip){

  var additional_options = {}
  if(limit)additional_options['limit'] = limit
  if(skip)additional_options['skip'] = skip

  return new Promise(function (result,error) {
    db.view(viewUrl,additional_options,function (err,docs) {
      if(docs){
        //var json=JSON.parse(JSON.stringify(docs));
        //var valueJson=[];
        //var request = JSON.parse(JSON.stringify(req));
        //var reqField = Object.keys(criteria)[0];
        var filteredDocs = find_in_object(docs, criteria);

        var filteredKeysResults = filteredDocs && filteredDocs.map(doc => doc.value).map(exlcude_keys(exclude_keys));

        // Sort by creation time
        filteredKeysResults.sort(function(a,b){
          // Turn your strings into dates, and then subtract them
          // to get a value that is either negative, positive, or zero.
          return -(new Date(b.date) - new Date(a.date));
        });

        return result(filteredKeysResults);
      }else if(err){
        return error(err);
      }
    })//end of get
  });//end of promise
};



var update= function(config) {
  return new Promise(function (result, error) {
    db.save(config, function (err, response) {
      if(response){
        result(response);
      }else if(err){
        error(error);
      }
    });
  });
};

var remove = function(configid) {
  return new Promise(function (result,error){
    db.remove(configid, function(err, response){
      if(response){
        result(response);
      }else if(err){
        error(err);
      }
    });
  });
};

module.exports.create = create;
module.exports.findById = findById;
module.exports.find = find;
module.exports.update = update;
module.exports.remove = remove;

