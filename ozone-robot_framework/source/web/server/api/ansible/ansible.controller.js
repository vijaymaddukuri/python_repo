/**
 * Using Rails-like standard naming convention for endpoints.
 * GET     /api/ansible              ->  index
 * POST    /api/ansible              ->  create
 * GET     /api/ansible/:id          ->  show
 * PUT     /api/ansible/:id          ->  update
 * DELETE  /api/ansible/:id          ->  destroy
 */

'use strict';

import _ from 'lodash';
import Ansible from './ansible.model';
import Project from '../../api/project/project.model';

var ansibletool = require('../../components/ansibletool/ansibletool');
var dbUtil = require('../../components/utils/dbutility');
var envconfig =  require('../../config/environment');
var kueapi = require('../../components/kue/kueAPI').kueAPI();
var encryption = require('../../components/encrypt/encrypt');

function respondWithResult(res, statusCode) {
  statusCode = statusCode || 200;
  return function(entity) {
    if (entity) {
      return res.status(statusCode).json(entity);
    }
  };
}

function saveUpdates(updates) {
  return function(entity) {
    //var updated = _.merge(entity, updates);
    var updated = dbUtil.updateDocument(entity,Ansible,updates);
    return Ansible.update(updated)
        .then( (result) => {
          return updated;
        });
  };
}

function removeEntity(res) {
  return function(entity) {
    if (entity) {
      return res.status(204).json(entity);
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
    return res.status(statusCode).send(err);
  };
}

/**
 * Get Total Rows
 * @param req
 * @param res
 */
export function totalRows(req, res){
  return Ansible.getTotalRows(function(totalRows){
    res.send(totalRows)
  }, function(err){
    res.status(500).send(err)
  })
}

/**
 * Get List of all Ansible Jobs
 * Filter by user, type, refid
 * Limit and skip options available
 * @param req
 * @param res
 * @returns {Promise.<TResult>}
 */
export function index(req, res) {
  var refid = req.query.refid;
  var projectId = req.query.projectId;

  var filterObject = {
    user:req.user.name
  };

  if(refid){
    filterObject.refid = refid;
  }

  if(projectId){
    filterObject.project = projectId;
  }

  // TODO: Filter out ansible results
  return Ansible.find(filterObject, ["ansibleResults","ansibleTasksToExecute"], req.query.limit, req.query.skip)
    .then(respondWithResult(res))
    .catch(handleError(res));

}

// Gets a single Ansible from the DB
/**
 * Find an existing job using jobId
 * @param {Object} req API Request containing jobID in URL
 * @param {Object} res API Response
 * @returns {*}
 */
export function show(req, res) {
  return Ansible.findById(req.params.id)
    .then(handleEntityNotFound(res))
    .then(respondWithResult(res))
    .catch(handleError(res));
}





/**
 * Get Logs for a job from Kue Processor
 * @param entity
 * @param successCallback
 * @param errorCallback
 */
var getKueLogs = function(entity,successCallback,errorCallback) {

  if(!entity.jobId){
    return console.log("Get Kue Processor logs for Job ID failed as Job ID is null" )
  }

  kueapi.getJobLogs(entity.jobId,function(response){
    successCallback(response);
  },function(response){
    errorCallback(response)
  });

  kueapi.getJob(entity.jobId,function(response){
    ansibletool.updateJobState(entity, response);
  },function(response){
    console.log("Get Keu Job Error =" + response)
  });

};


/**
 * Get Logs for a given job
 * @param {Object} req API Request containing jobID in URL
 * @param {Object} res API Response
 * @returns {*}
 */
export function getLogs(req, res) {
  return Ansible.findById(req.params.id)
    .then(handleEntityNotFound(res))
    .then(function(entity){
      if (!entity.jobId){
        return res.status(500).send('No log file registered for this task')
      }

      getKueLogs(entity,
        function(successData){
          return res.send(successData);
        },
        function(errorData){
          console.log("Error " + errorData);
          return res.status(500).send(errorData)
        }
      );
      return null;
    })
    .catch(handleError(res));
}

/**
 * Execute Ansible Job
 * @param req
 * @param res
 * @param logfilename
 * @param AnsibleType
 * @param AnsibleData
 * @param tags_joined
 * @param limit_to_hosts_joined
 * @param verbose
 * @param check_mode
 * @param extra_vars
 * @param decryptedVaultPassword
 * @returns {Function}
 */
function executeAnsibleJob(req, res, logfilename, AnsibleType, AnsibleData, tags_joined, limit_to_hosts_joined, verbose, check_mode, extra_vars, decryptedVaultPassword){
  return function(entity){
    if(entity){
      try{
        ansibletool.executeAnsible(entity, req.user.name, logfilename, AnsibleType, AnsibleData.project.name,tags_joined, limit_to_hosts_joined, verbose, check_mode, extra_vars,
          function(data){
            //If job started
            entity.state = "active";
            entity.jobId = data.id;
            entity.ansibleTasksToExecute = data.ansibleTasksToExecute;
            Ansible.update(entity).then(result => {
              return res.send(entity);
            });

            try{
              // If restore EHC job mark restore type
              if(AnsibleType.indexOf("_rollback-ehc") > -1){
                Project.findById(AnsibleData.project._id)
                  .then(function(entity){
                    console.log("-------------------------------------------------" + JSON.stringify(AnsibleData.extra_vars))
                    console.log("AnsibleData.extra_vars.EHC_REVERT_TO_STATE =" + AnsibleData.extra_vars.EHC_REVERT_TO_STATE)
                    entity.restorePoint = AnsibleData.extra_vars.EHC_REVERT_TO_STATE;
                    Project.update(entity);
                  })
              }else{
                Project.findById(AnsibleData.project._id)
                  .then(function(entity){
                    entity.restorePoint = null;
                    Project.update(entity);
                  })
              }
            }catch(e){
              console.error("Unable to update project with restore ehc data" + e)
            }
          },
          function(error, body){
            //If job didnt start
            entity.state = "Error";
            entity.errorData = error + body;
            Ansible.update(entity).then(result => {
              return res.status(500).json({error:entity.errorData});
            })
          }, null, decryptedVaultPassword, AnsibleData.project._id);

      } catch (e) {
        console.log("Error " + e);
        return res.status(500).send(e);
      }
    }
  }
}


/**
 * Execute Ansible Orchestration Task
 *
 * @param {Object} req API Request containing Ansible playbook information
 * @param {Object} res API Response
 */
export function ansibleExecute(req, res) {

  if(!global.serverCache.get('masterPassword')){
    return res.status(500).send("Master Password not Set")
  }

  var decryptedVaultPassword = global.serverCache.get('masterPassword');

  var AnsibleData = req.body;
  var AnsibleType = AnsibleData.type;
  var time = new Date().getTime();
  var logfilename = 'Ansible_' + AnsibleType.join('_') + '_' + req.user.name.replace(" ","_") + '_' + time + '.log';
  //var decryptedVaultPassword = encryption.decrypt(AnsibleData.project.components.import_data.vars.common.vault_password, AnsibleData.project.components.encryptionKey);


  var tags = AnsibleData.tags;
  var limit_to_hosts = AnsibleData.limit_to_hosts;
  var verbose = AnsibleData.verbose;
  var check_mode = AnsibleData.check_mode;
  var extra_vars = AnsibleData.extra_vars || null;

  var tags_joined = tags;
  if(typeof tags === 'object')tags_joined = tags.join(',');

  var limit_to_hosts_joined = limit_to_hosts;
  if(typeof limit_to_hosts === 'object')limit_to_hosts_joined = limit_to_hosts.join(',');

  var AnsibleObject= {
    name: AnsibleType.join('_'),
    info: {
      tags : AnsibleData.tags,
      limit_to_hosts : AnsibleData.limit_to_hosts,
      verbose : AnsibleData.verbose,
      check_mode : AnsibleData.check_mode
    },
    execType: 'Ansible',
    user: req.user.name,
    userInfo: req.user,
    type: AnsibleType.join('_'),
    logfile: logfilename,
    project: AnsibleData.project._id,
    date: new Date(),
    refid: AnsibleData.refid,
    doc_type: 'ansible'
  };

  Ansible.create(AnsibleObject)
    .then(function(result) {
      Ansible.findById(result.id)
        .then(executeAnsibleJob(req, res, logfilename, AnsibleType, AnsibleData, tags_joined, limit_to_hosts_joined, verbose, check_mode, extra_vars, decryptedVaultPassword))
    })
    .catch(handleError(res));

  // TODO: Temporarily disabling as check has some issues.
  // // Check agent connectivity before starting ansible job
  //
  // var frameworkUtils = require('../../components/debug/framework');
  //
  // frameworkUtils.checkAgentConnectivity(function(){
  //
  // }, function(error){
  //   res.status(500).send(error)
  // });


}



/**
 * Get Roolback Points
 * @param req
 * @param res
 */
export function getRollbackPoints(req, res){

  var AnsibleData = req.body;
  var AnsibleType = AnsibleData.type;
  var projectName = AnsibleData.project.name;

  ansibletool.getRollbackPoints(req.user, projectName,
    function(response){
      res.send(response)
    },
    function(errorResponse){
      res.status(500).send(errorResponse)
    });

}

/**
 * List Ansible Tasks given a component
 * @param {Object} req API Request
 * @param {Object} res API Response
 */
export function ansibleListTasks(req, res){

  var AnsibleData = req.body;
  var AnsibleType = AnsibleData.type;
  var projectName = AnsibleData.project.name;
  var extra_vars = AnsibleData.extra_vars || null;
  //var decryptedVaultPassword = encryption.decrypt(AnsibleData.project.components.import_data.vars.common.vault_password, AnsibleData.project.components.encryptionKey);

  if(!global.serverCache.get('masterPassword')){
    return res.status(500).send("Master Password not Set")
  }

  var decryptedVaultPassword = global.serverCache.get('masterPassword');

  ansibletool.getAnsibleTasks(req.user, projectName, AnsibleType,
    function(response){

      var tasks_re = /[^{]*({[^]+})[^]+?/g;
      var tasksText = response.replace(tasks_re,'$1');

      res.send(tasksText)
    },
    function(errorResponse){
      res.status(500).send(errorResponse)
    }, decryptedVaultPassword, extra_vars);

}

/**
 * Ansible List Playbooks
 * @param req {Object} req API Request
 * @param res {Object} res API Response
 */
export function ansibleListPlaybooks(req, res){

  var AnsibleData = req.body;
  var projectName = AnsibleData.project.name;

  ansibletool.getAnsiblePlaybooks(req.user, projectName,
    function(response){
      res.send(response)
    },
    function(errorResponse){
      res.status(500).send(errorResponse)
    });

}

// Updates an existing Ansible in the DB
export function ansibleStop(req, res) {
  var AnsibleData = req.body;

  return Ansible.findById(AnsibleData._id)
    .then(handleEntityNotFound(res))
    .then(saveUpdates({'state':'stopping'}))
    .then(function(entity){
      kueapi.stopJob(entity.jobId, entity._id, function(){
        res.send(entity);
      }, handleError(res));

    })
    .catch(handleError(res));
}

/**
 * Kill Ansible Job
 * @param req
 * @param res
 * @returns {Promise.<TResult>}
 */
export function ansibleKill(req, res) {
  var AnsibleData = req.body;

  return Ansible.findById(AnsibleData._id)
    .then(handleEntityNotFound(res))
    .then(saveUpdates({'state':'killing'}))
    .then(function(entity){
      kueapi.killJob(entity.jobId, entity._id, function(){
        res.send(entity);
      }, handleError(res));

    })
    .catch(handleError(res));
}

// Updates an existing Ansible in the DB
export function update(req, res) {
  if (req.body._id) {
    delete req.body._id;
  }
  return Ansible.findById(req.params.id)
    .then(handleEntityNotFound(res))
    .then(saveUpdates(req.body))
    .then(respondWithResult(res))
    .catch(handleError(res));
}

// Deletes a Ansible from the DB
export function destroy(req, res) {
  return Ansible.remove(req.params.id)
    .then(removeEntity(res))
    .catch(handleError(res));
}
