/**
 * Sample programe to cleanup Kue
 */

//var envconfig = require('../../config/environment');

var kue = require('kue'),
  queue = kue.createQueue({redis: {host:'localhost', auth: 'P@ssw0rd@123'}});
// Check and set password separately

kue.Job.rangeByState('complete', 0, 20000, 'asc', function (err, jobs) {
  console.log("Jobs = ", jobs.length);
  jobs.forEach(function (job) {
    console.log("re-moving job " + job.id);
    job.remove(function () {
      console.log('removed ', job.id);
    });
  });
});

