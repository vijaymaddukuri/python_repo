
var appconfig = require('../../config/environment/development');
var couchStore = require('../../components/dbConnect/couchdbConnect');
var db = couchStore.getCouchConnection(appconfig.couch.server,appconfig.couch.port,appconfig.couch.database);
const viewUrl = 'collections/ansible';

/**
 * Find in Object
 * @param my_object
 * @param my_criteria
 * @returns {Array.<T>|*}
 */
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


var testDBCount = function() {
  var db2 = couchStore.getCouchConnection(appconfig.couch.server,appconfig.couch.port,appconfig.couch.database,true);
  db2.view(viewUrl, {limit: 0}, function (err, docs) {
    console.log(docs);
  })
}

var testDB = function(criteria, exclude_keys){
  db.view(viewUrl,{keys:['_id'],limit:5}, function (err,docs) {
    if(docs){
      //var json=JSON.parse(JSON.stringify(docs));
      //var valueJson=[];
      var filteredDocs = find_in_object(docs.rows, criteria);
      //
      var filteredKeysResults = filteredDocs && filteredDocs.map(doc => doc.value).map(exlcude_keys(exclude_keys));
      //
      // // Sort by creation time
      // filteredKeysResults.sort(function(a,b){
      //   // Turn your strings into dates, and then subtract them
      //   // to get a value that is either negative, positive, or zero.
      //   return -(new Date(b.date) - new Date(a.date));
      // });

      console.log(JSON.stringify(filteredKeysResults,null,'\t'));

    }else if(err){
      console.log(err);
    }
  })

}


var criteria = {
  _id: '5ef4f95b3cd52ab88bee63316a0036a6'
}

var exclude_keys = ['ansibleTasksToExecute']

testDB(criteria, exclude_keys)
//testDBCount()
