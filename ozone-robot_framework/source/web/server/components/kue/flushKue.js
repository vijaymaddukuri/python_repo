/**
 * Sample programe to requeue tasks in Kue
 */

//var envconfig = require('../../config/environment');

var kue = require('kue'),
  queue = kue.createQueue({redis:{host:'localhost', auth: 'P@ssw0rd@123'}});
  // Check and set password separately

queue.inactiveCount('exec', function(err, count){

  console.log("count =" + count);
  queue.shutdown(function(){
    console.log("Shutdown")
  })
});

// queue.active( function( err, ids ) {
//   ids.forEach( function( id ) {
//     kue.Job.get( id, function( err, job ) {
//       // Your application should check if job is a stuck one
//         if(job.type === "statusUpdate"){
//           console.log("Re-queuing job " + id);
//           job.inactive();
//         }
//     });
//   });
// });

