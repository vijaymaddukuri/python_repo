var cradle = require('cradle');

exports.createCouchDB = function(server,port, database,userName,password,successCallback,errorCallback) {
  const dbName = database;

  var c = new (cradle.Connection)(server, port, {
    //auth: {username: userName, password: password}
  });

  var db = c.database(dbName);

  db.exists(function (err, exists) {
    if (err) {
      console.log('Error ---> ', err);
      errorCallback(err);
    } else if (exists) {
      console.log('Database already exists. Not creating any views.');
    } else {
      console.log('Database does not exists. Creating new database.');
      db.create(function (error) {
        if (!error) {
          console.log('Database creation successful. Creating views...');
          db.save('_design/collections', {
            ansible: {
                "map": "(function (doc) {if (doc.doc_type === 'ansible') { emit(null, {\
                _id:doc._id,\
                execType:doc.execType,\
                user:doc.user,\
                refid:doc.refid,\
                project:doc.project,\
                ansibleState: doc.ansibleState,\
                duration: doc.duration,\
                execType: doc.execType,\
                state: doc.state,\
                type: doc.type,\
                date: doc.date,\
                jobId: doc.jobId,\
                name: doc.name,\
                tasks: doc.ansibleTasksToExecute.length\
              });\
            }})"
            },
            log: {
              "map": "(function (doc) {if (doc.doc_type === 'log') { emit(null, doc); }})"
            },
            project: {
              "map": "(function (doc) {if (doc.doc_type === 'project') { emit(doc.user, doc); }})"
            },
            snapshot: {
              "map": "(function (doc) {if (doc.doc_type === 'snapshot') { emit(null, doc); }})"
            },
            upgrade: {
              "map": "(function (doc) {if (doc.doc_type === 'upgrade') { emit(null, doc); }})"
            },
            user: {
              "map": "(function (doc) {if (doc.doc_type === 'user') { emit(null, doc); }})"
            }
          }); //end save
        } else{
          console.log(' Error in creating database --->' + error);
        }//end if
      });  //end create
    } // end of else
  }); //end of exists
};

/**
 * Create a new Couch Connection
 * @param server
 * @param port
 * @param database
 * @returns {*}
 */
exports.getCouchConnection = function(server,port, database, raw) {

  cradle.setup({
    host: server,
    cache: true,
    raw: raw,
    forceSave: true
  });

  var c=new(cradle.Connection)();
  var db=c.database(database);
  return db;
}
