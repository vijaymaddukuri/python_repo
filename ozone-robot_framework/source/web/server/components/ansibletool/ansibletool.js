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


/**
 * Created by mannam4 on 9/16/2016.
 */

/// TODO: Remove this line during production
process.env.NODE_ENV = 'development';

var ssh2_exec = require('../ssh/ssh2_exec');
var scp_exec = require('../scp/scp_exec');
var config =  require('../../config/environment');
var async = require('async');
var YAML = require('yamljs');
var kueAPIClass = require('../../components/kue/kueAPI');
var kueapi = kueAPIClass.kueAPI();
var logFile = 'logs/ansible/general.log';
var Ansible = require('../../api/ansible/ansible.model');

//var vault_password_file_option = ' --vault-password-file ~/.vault_pass.txt';
//var vault_password_file_option = ' --ask-vault-pass';
var vault_password_file_option =  ' --vault-password-file /opt/ozone-scripts/scripts/vault-pass-script.sh'
var dbUtil = require('../../components/utils/dbutility');

import Project from '../../api/project/project.model';

/**
 * Create Projects Folder if not exists
 * @param user
 * @param asyncCallback
 * @param errorCallback
 */
exports.createProjectsFolder = function(user, asyncCallback, errorCallback){
  var command = 'mkdir -p ' + config.scriptEngine.projectsFolder;

  console.log("Create Projects Folder " + command);

  ssh2_exec.executeCommand(user, command, logFile, null,
    function(response){
      asyncCallback();
    },
    function(errorResponse){
      errorCallback(errorResponse);
      //Don't go further
      asyncCallback(true)
    });
};

/**
 * Create folder on script engine
 * @param user
 * @param folderPath
 * @param asyncCallback
 * @param errorCallback
 */
exports.createFolder = function(user, folderPath, asyncCallback, errorCallback){
  var command = 'mkdir -p "' + folderPath + '"';

  ssh2_exec.executeCommand(user, command, logFile, null,
    function(response){
      asyncCallback();
    },
    function(errorResponse){
      errorCallback(errorResponse);
      //Don't go further
      asyncCallback(true)
    });
};

/**
 * Encrypt YAML file
 * @param user - User Name
 * @param filePath - Location of YAML file to encrypt on script engine
 * @param asyncCallback
 * @param errorCallback
 */
exports.encryptYamlFile = function(user, filePath, asyncCallback, errorCallback, decryptedVaultPassword){

  var command = 'export ANSIBLE_VAULT_PASSWORD=' + decryptedVaultPassword + '; ' +
                'ansible-vault encrypt "' + filePath + '" ' + vault_password_file_option;

  ssh2_exec.executeCommand(user, command, logFile, null,
    function(response){
      asyncCallback();
    },
    function(errorResponse){
      errorCallback(errorResponse);
      //Don't go further
      asyncCallback(true)
    });

};

/**
 * Create Project Folder
 * @param user
 * @param projectName
 * @param asyncCallback
 * @param errorCallback
 * @param completeCallback
 */
exports.createProjectFolder = function(user, projectName, asyncCallback, completeCallback, errorCallback){
  var command = 'mkdir "' + config.scriptEngine.projectsFolder + projectName + '"';

  console.log("createProjectFolder " + command);

  ssh2_exec.executeCommand(user, command, logFile, null,
    function(response){
      //completeCallback(response);
      asyncCallback();
    },
    function(errorResponse){
      errorCallback(errorResponse);
      //Don't go further
      asyncCallback(true)
    });
};

/**
 * Copy Ansible Projects Template to the new folder
 * - Ansible EHC Project Template that contains pre created roles and playbooks
 * @param user
 * @param projectName
 * @param projectType
 * @param asyncCallback
 * @param errorCallback
 * @param completeCallback
 */
exports.copyAnsibleProjectTemplate = function(user, projectName, projectType, asyncCallback, completeCallback, errorCallback){

  console.log("Copy ansible project template for project " + projectName);

  var command = 'cd "' + config.scriptEngine.projectsFolder + projectName + '";' +
                'rsync -av ' + config.scriptEngine.ansibleProjectTemplates + projectType + '/ ./ --exclude "playbooks/backup_and_restore/rollback-points.yml"';

  // To get rid of rsync
  // var command = 'mkdir -p "' + config.scriptEngine.projectsFolder + projectName + '";' +
  //               'cp -r "' + config.scriptEngine.ansibleProjectTemplates + projectType + '/"* "' + config.scriptEngine.projectsFolder + projectName + '"';

  console.log("Command =" + command);

  ssh2_exec.executeCommand(user, command, logFile, null,
    function(response){
      completeCallback(response);
      asyncCallback();
    },
    function(errorResponse){
      errorCallback(errorResponse);
      //Don't go further
      asyncCallback(true)
    });
};


/**
 * Create Ansible Project
 * - Create project folder
 * - Copy Ansible project template
 * @param user
 * @param projectName
 * @param projectType
 * @param completeCallback
 * @param errorCallback
 */
exports.createProject = function(user, projectName, projectType, completeCallback,errorCallback){

  async.series([
    asyncCallback => {
      // Create base projects folder if it doesn't exists.
      exports.createProjectsFolder(user, asyncCallback, errorCallback)
    },
    // asyncCallback => {
    //   // Create Project folder. Error if project already exists.
    //   exports.createProjectFolder(user, projectName, asyncCallback, completeCallback, errorCallback)
    // },
    asyncCallback => {
      // Copy Ansible Project Template
      exports.copyAnsibleProjectTemplate(user, projectName, projectType, asyncCallback, completeCallback, errorCallback);

    }
  ],err => {
    // Code to execute when everything is done.
    if(err){
      console.log("Error in async series")
    }
  });
};


/**
 * Check if a given folder exists on Ansible Engine
 * @param user
 * @param folderPath
 * @param completeCallback
 * @param errorCallback
 */
exports.checkIfFolderExists = function(user, folderPath, completeCallback, errorCallback){

  var command = 'ls "' + folderPath + '"';

  ssh2_exec.executeCommand(user, command, logFile, null,completeCallback, errorCallback);
};

/**
 * Check if Project Folder Exists
 * @param user
 * @param projectName
 * @param projectType
 * @param asyncCallback
 * @param completeCallback
 * @param errorCallback
 */
exports.checkProjectFolder = function(user, projectName, projectType, asyncCallback, completeCallback, errorCallback){
  var command = 'ls "' + config.scriptEngine.projectsFolder + projectName + '"';

  exports.createProject(user, projectName, projectType, completeCallback,errorCallback);

  // exports.checkIfFolderExists(user, config.scriptEngine.projectsFolder + projectName,
  //   function(response){
  //   completeCallback();
  //
  // }, function(errorResponse){
  //     console.log("Creating Project Folder");
  //
  // });

};


/**
 * Create Inventory file and add contents
 * @param user
 * @param projectName
 * @param projectType
 * @param inventoryFileName
 * @param inventoryFileContents
 * @param completeCallback
 * @param errorCallback
 */
exports.createInventoryFile = function(user, projectName, projectType, inventoryFileName, inventoryFileContents, completeCallback, errorCallback){

  async.series([
    asyncCallback => {
      // Check if project folder exists. If not create project folder
      exports.checkProjectFolder(user, projectName, projectType, asyncCallback, function(response){
        asyncCallback()
      }, errorCallback)
    },
    asyncCallback => {
      // Copy Ansible Project Template
      var destinationPath = config.scriptEngine.projectsFolder + projectName + '/inventory';
      scp_exec.createFileOnScriptEngine(inventoryFileContents,destinationPath,completeCallback,errorCallback);
      asyncCallback()
    }
  ],err => {
    // Code to execute when everything is done.
    if(err){
      console.log("Error in async series")
    }
  });
};

/**
 * Update Common Roles Variables
 * - Overwrites contents!
 * @param user
 * @param projectName
 * @param projectType
 * @param commonVariableContents
 * @param dynamic_hosts_string
 * @param completeCallback
 * @param errorCallback
 */
exports.updateCommonVariables = function(user, projectName, projectType, commonVariableContents, dynamic_hosts_string, completeCallback, errorCallback, decryptedVaultPassword){

  //var commonsFolderPath = config.scriptEngine.projectsFolder + projectName + '/roles/common/vars';
  //var destinationPath = commonsFolderPath + '/main.yml';

  console.log("Update common variables " + projectType);

  var destinationFolder = config.scriptEngine.projectsFolder + projectName;
  var destinationPath = destinationFolder + '/group_vars/all/all';

  async.series([
    asyncCallback => {
      // Check if project folder exists. If not create project folder
      exports.checkProjectFolder(user, projectName, projectType, asyncCallback, function(response){
        asyncCallback()
      }, errorCallback)
    },
    asyncCallback => {
      // Check if project folder exists. If not create project folder

      exports.createFolder(user, destinationFolder, asyncCallback, errorCallback)
    },
    asyncCallback => {
      scp_exec.createFileOnScriptEngine(commonVariableContents,destinationPath,function(response){
        asyncCallback()
      }, errorCallback);
    },
    asyncCallback => {
      // Update Log Insight and vROPS workers inventory file
      if(dynamic_hosts_string){
        var dynamicInventoryPath = destinationFolder + '/inventory/dynamic_hosts';
        scp_exec.createFileOnScriptEngine(dynamic_hosts_string,dynamicInventoryPath,function(response){
          asyncCallback()
        }, errorCallback);
      }else{
        asyncCallback();
      }

    },
    asyncCallback => {
      // Encrypt YAML File
      exports.encryptYamlFile(user, destinationPath, asyncCallback, errorCallback,decryptedVaultPassword);
    },
    asyncCallback => {
      // Check if project folder exists. If not create project folder
      completeCallback();
      asyncCallback()
    },
  ],err => {
    // Code to execute when everything is done.
    if(err){
      console.log("Error in async series")
    }
  });

};

/**
 * Get Hosts by Name
 * @param hosts
 * @param name
 */
var get_hosts_by_name = function(hosts, name){

  if(!hosts)return null;

  var results = [];
  Object.keys(hosts).forEach((host) => {
    if(host.indexOf(name) > -1){
      results.push(host)
    }
  });

  return results;

};

/**
 * Update Ansible Variable Files
 * @param user
 * @param project
 * @param completeCallback
 * @param errorCallback
 */
exports.updateAnsibleVariableFiles = function(user, project,completeCallback,errorCallback){

  if(project && project.components && project.components.import_data && project.components.import_data.vars){
    var yamlString;
    try{
      yamlString = YAML.stringify(project.components.import_data.vars, 100);
    }catch(ex){
      return errorCallback("Unable to convert data into YAML format " + ex);
    }

    var dynamic_hosts_string = '';

    // TODO: Improve this and modularize.
    // Generate dynamic hosts file
    if(project.components.import_data.vars.host_address){
      var log_insight_worker_hosts = get_hosts_by_name(project.components.import_data.vars.host_address, 'log_insight_worker');
      var log_insight_forwarder_hosts = get_hosts_by_name(project.components.import_data.vars.host_address, 'log_insight_forwarder');
      var vrops_data_hosts = get_hosts_by_name(project.components.import_data.vars.host_address, 'vrops_data_node');
      var vrops_remote_collector_hosts = get_hosts_by_name(project.components.import_data.vars.host_address, 'vrops_remote_collector_node');


      if(log_insight_worker_hosts && log_insight_worker_hosts.length){
        dynamic_hosts_string = '[log_insight_workers]\n' + log_insight_worker_hosts.join('\n');
      }

      if(vrops_data_hosts && vrops_data_hosts.length){
        dynamic_hosts_string += '\n\n[vrops_data_nodes]\n' + vrops_data_hosts.join('\n');
      }

      if(vrops_remote_collector_hosts && vrops_remote_collector_hosts.length){
        dynamic_hosts_string += '\n\n[vrops_remote_collectors]\n' + vrops_remote_collector_hosts.join('\n');
      }

      if(log_insight_forwarder_hosts && log_insight_forwarder_hosts.length){
        dynamic_hosts_string += '\n\n[log_insight_forwarders]\n' + log_insight_forwarder_hosts.join('\n');
      }

    }

    console.log("Calling Update common variables " + project.type);

    this.updateCommonVariables(user.name, project.name, project.type, yamlString, dynamic_hosts_string, completeCallback, errorCallback, project.components.import_data.vars.common.vault_password);

  }

};


/**
 * Get Tasks List From Logs
 * @param ansibleOutput
 */
var getTasksListFromLogs = function(ansibleOutput){

  if(!ansibleOutput)return;

  var tasks_re = /[^{]*({[^]+})[^]+?/g;

  //TODO: Improvise
  var tasksText = ansibleOutput.replace(tasks_re,'$1');

  var tasksObject;
  var tasksList = [];
  var playList = [];

    tasksObject = JSON.parse(tasksText.replace(/\r\n/g,"").replace(/\r/g,"").replace(/\n/g,""));

    for(var i=0; i < tasksObject.playbooks.length; i++){
      var playbook = tasksObject.playbooks[i];
      for(var j=0; j < playbook.plays.length; j++){
        var play = playbook.plays[j];
        for(var k=0; k < play.tasks.length; k++){
          var task = play.tasks[k];

          var taskName = task.name;
          if(task.name && task.name.indexOf(":") > -1){
            taskName = taskName.split(":")[1].trim()
          }

          tasksList.push({playName: play.name, taskName: taskName, status: 'QUEUED'})

        }
      }
    }

    return tasksList;
};

/**
 * Update Ansible Job State
 * @param ansibleJob
 * @param jobResponse
 * @param Timeout
 * @param projectId
 */
exports.updateJobState = function(ansibleJob, jobResponse, Timeout, projectId){
  if(ansibleJob.state !== 'stopping' && ansibleJob.state !== 'killing'){
    ansibleJob.state = jobResponse.state;
  }

  if(kueapi.kueTerminalStates.indexOf(jobResponse.state) > -1){
    if(ansibleJob.state === 'stopping'){
      ansibleJob.state = 'stopped';
    }
    if(ansibleJob.state === 'killing'){
      ansibleJob.state = 'killed';
    }
    else{
      ansibleJob.state = jobResponse.state;
    }

    // Clear poll if setup
    Timeout && clearInterval(Timeout);
  }

  if(jobResponse.state === 'failed'){
    // Calculate Job Duration
    ansibleJob.duration = (jobResponse.failed_at || jobResponse.updated_at) - jobResponse.started_at;

    // Send notification email
    try{
      sendNotificationEmail(projectId);
    }catch(e){
      console.warn("Failed to send notification email " + e);
    }

  }
  else ansibleJob.duration = jobResponse.duration;

  Ansible.update(ansibleJob).then(result => {
    return entity;
  });
};

/**
 * Send Notification email
 * @param projectId
 */
var sendNotificationEmail = function(projectId){
  Project.findById(projectId)
    .then(function(entity){
      if(entity.components.import_data.vars.smtp){
        var frameworkUtils = require('../../components/debug/framework');
        console.log("Sending email notification");
        frameworkUtils.sendEmailNotificationViaAgent(entity.components.import_data.vars.smtp, entity.components.encryptionKey, function(){
          console.log("Successfully sent email notification")
        }, function(error){
          console.error("Error sending email notification " + error)
        });
      }

    });
};

/**
 * Monitor Kue Job and update database with the state
 * @param jobId - Job ID to monitor
 * @param ansibleJobId - Ansible Job ID to update
 * @param monitorIntervalSec - Monitor Interval in Seconds. Defaults to 10 seconds
 * @param projectId - Project ID
 */


var monitorAnsibleJob = function(jobId, ansibleJobId, monitorIntervalSec, projectId){

  monitorIntervalSec = monitorIntervalSec || 10;

  var Timeout = setInterval(function(){
    console.log('Monitoring Job' + jobId);

    kueapi.getJob(jobId,function(response){

      Ansible.findById(ansibleJobId)
        .then(function(ansibleJob) {
          exports.updateJobState(ansibleJob, response, Timeout, projectId);
        });


    }, function(response){
      console.error("Get Keu Job Error =" + response)
    });

  }, monitorIntervalSec * 1000);


};

/**
 * Generate ansible execution command and execute ansible
 * @param playbook_name
 * @param ansibleObject
 * @param user
 * @param logfilename
 * @param ansiblePlaybooks
 * @param projectName
 * @param tags_joined
 * @param limit_to_hosts_joined
 * @param verbose
 * @param check_mode
 * @param extra_vars
 * @param successCallback
 * @param errorCallback
 * @param ansibleEngine
 * @param decryptedVaultPassword
 * @param projectId
 * @private
 */
var _executeAnsible = function(playbook_name, ansibleObject, user, logfilename, ansiblePlaybooks, projectName, tags_joined, limit_to_hosts_joined, verbose,check_mode, extra_vars, successCallback,errorCallback,ansibleEngine,decryptedVaultPassword, projectId){
  extra_vars = extra_vars || {};
  var inventory_file_name = 'inventory';

  var command_prefix = '' +
    'export ANSIBLE_FORCE_COLOR=True; export ANSIBLE_HOST_KEY_CHECKING=False; ' +
    'export ANSIBLE_CALLBACK_PLUGINS=callback_plugins; ' +
    'export KUE_HOSTNAME=' + config.kue.host + '; ' +
    'export KUE_PORT=' + config.kue.port + '; ' +
    'export OZONE_HOSTNAME=' + '127.0.0.1' + '; ' +
    'export OZONE_PORT=' + process.env.PORT + '; ' +
    'export OZONE_USERNAME=ansibleozoneconnect@ozone.com; ' +
    'export OZONE_PASSWORD=ansibleConnect; ' +
    'export OZONE_ANSIBLE_ID=' + ansibleObject._id + '; ' +
    'export OZONE_REDIS_PASSWORD=' + global.serverCache.get('masterPassword') + '; ' +
    'export ANSIBLE_VAULT_PASSWORD=' + decryptedVaultPassword + '; ' +
    'cd "' + config.scriptEngine.projectsFolder + projectName + '"; ';

  var command = 'ansible-playbook "' + playbook_name + '" -i "' + inventory_file_name + '" ';

  var options = vault_password_file_option;

  if(tags_joined)
    options += ' --tags "' + tags_joined + '"';

  if(limit_to_hosts_joined)
    options += ' --limit "' + limit_to_hosts_joined + '"';

  if(verbose === 'verbose_connection'){
    options += ' -vvvv ';
  }
  if(verbose === 'verbose_detail'){
    options += ' -vvv ';
  }
  else if(verbose === 'verbose'){
    options += ' -v ';
  }

  if(check_mode !== 'No_Check'){
    options += ' --check ';
  }

  // If playbook is a Master playbook, set extra variable to enable saving list of good configurations in roles/common/defaults/vars.yml file
  // This is part of Backup and Restore feature
  if(playbook_name.indexOf('Master') > -1 || playbook_name.indexOf('MASTER') > -1){
    extra_vars.ENABLE_SAVE_GOOD_CONFIGURATIONS = true;
  }


  if(extra_vars){
    options += ' --extra-vars \''+ JSON.stringify(extra_vars) +'\''
  }

  var list_tasks_command = 'python /opt/ozone-scripts/ehc-python-modules/ansible_modules/my_playbook.py "' + playbook_name + '" -i "' + inventory_file_name + '" ' +
    ' ' + options + ' --list-tasks-json --list-hosts;';

  var execute_command = command + ' ' + options;

  var final_command = command_prefix + execute_command;

  var logFile = 'logs/ansible/' + logfilename;

  ssh2_exec.executeCommand(user, command_prefix + list_tasks_command, logFile, null,
    function(response){
      var ansibleTasksToExecute;
      try{
        ansibleTasksToExecute = getTasksListFromLogs(response);
      }catch(ex){
        return errorCallback("Error getting Task list to execute - " + ex)
      }

      // Send Ansible job to Queue for Execution
      kueapi.runJob({
        type:'exec',
        data:{
          title: 'Ansible Playbook -' + ansibleObject.type,
          "command": final_command,
          "id" : ansibleObject._id
        }
      }, function(response){
        response.ansibleTasksToExecute = ansibleTasksToExecute;
        successCallback(response);
        monitorAnsibleJob(response.id, ansibleObject._id, null, projectId);
    }, function(response, body){
        errorCallback(response, body)
      });

    },
    function(errorResponse){
      errorCallback(errorResponse)
    });

};

/**
 * Prepare Temporary playbook for running multiple playbooks one after the other
 * @param ansiblePlaybooks
 * @param projectName
 * @param user
 * @param completeCallback
 * @param errorCallback
 */
var prepareTemporaryPlaybook = function(ansiblePlaybooks, projectName, user, completeCallback, errorCallback){
  var playbook_name;
  var includeContent = ansiblePlaybooks.map(ansiblePlaybook => {
    return '- include: ' + ansiblePlaybook + '.yml'
  });

  var tempPlaybookContent = '---\n' +
    '# Temporary Playbook file for combining: ' + ansiblePlaybooks.join(',') + '\n' +
    includeContent.join("\n");
  playbook_name = 'tmp_playbook_' + new Date().getTime() + '.yml';


  var destinationPath = config.scriptEngine.projectsFolder + projectName + '/' + playbook_name;

  scp_exec.createFileOnScriptEngine(tempPlaybookContent,destinationPath,function(){
    completeCallback(playbook_name, destinationPath)
  },errorCallback);
};

/**
 * Execute Ansible Playbook
 * @param ansibleObject
 * @param user
 * @param logfilename
 * @param ansiblePlaybooks
 * @param projectName
 * @param tags_joined
 * @param limit_to_hosts_joined
 * @param verbose
 * @param check_mode
 * @param extra_vars
 * @param successCallback
 * @param errorCallback
 * @param ansibleEngine
 * @param decryptedVaultPassword
 * @param projectId
 */
exports.executeAnsible = function(ansibleObject, user, logfilename, ansiblePlaybooks, projectName, tags_joined, limit_to_hosts_joined, verbose,check_mode, extra_vars, successCallback,errorCallback,ansibleEngine,decryptedVaultPassword, projectId){
  var playbook_name;

  var projectFolder = '"' + config.scriptEngine.projectsFolder + projectName + '"';

  if(!ansiblePlaybooks)return errorCallback('No ansible type specified. Must be file name of an Ansible Playbook(s)');
  if(ansiblePlaybooks && ansiblePlaybooks.length === 1) {
    playbook_name =ansiblePlaybooks[0] + '.yml';
    _executeAnsible(playbook_name, ansibleObject, user, logfilename, ansiblePlaybooks, projectName, tags_joined, limit_to_hosts_joined, verbose,check_mode, extra_vars, successCallback,errorCallback,ansibleEngine,decryptedVaultPassword,projectId);
  }
  else {
    prepareTemporaryPlaybook(ansiblePlaybooks, projectName, user, function(playbook_name, destinationPath) {
      _executeAnsible(playbook_name, ansibleObject, user, logfilename, ansiblePlaybooks, projectName, tags_joined, limit_to_hosts_joined, verbose, check_mode, extra_vars, successCallback, errorCallback, ansibleEngine,decryptedVaultPassword,projectId);
    }, errorCallback);
  }

};

/**
 * Get List of Ansible Playbooks
 * @param user
 * @param projectName
 * @param completeCallback
 * @param errorCallback
 */
exports.getAnsiblePlaybooks = function(user, projectName, completeCallback, errorCallback){

  var projectFolder = '"' + config.scriptEngine.projectsFolder + projectName + '"';

  var command = 'ls ' + projectFolder + ' | grep "^[^_]*.yml"';
  var ansiblePlaybookListResults = "";

  ssh2_exec.executeCommand(user, command, logFile, null,
    function(response){
      // Folder Exists
      ansiblePlaybookListResults=response;
      var files = [];
      if(ansiblePlaybookListResults)
        files = ansiblePlaybookListResults.trim().split('\n');
      completeCallback(files);
    },
    function(errorResponse){
      errorCallback(errorResponse)
    });

};

/**
 * Generate command and execute getAnsible Tasks to list tasks
 * @param projectFolder
 * @param playbook_name
 * @param user
 * @param completeCallback
 * @param errorCallback
 * @param decryptedVaultPassword
 * @private
 */
var _getAnsibleTasks = function(projectFolder, playbook_name, user, completeCallback,errorCallback, decryptedVaultPassword, extra_vars){
  var inventory_file_name = 'inventory';

  var command = 'export ANSIBLE_HOST_KEY_CHECKING=False;' +
    'export ANSIBLE_VAULT_PASSWORD=' + decryptedVaultPassword + '; ' +
    'cd ' + projectFolder + ';' +
    'python /opt/ozone-scripts/ehc-python-modules/ansible_modules/my_playbook.py "' + playbook_name + '" -i "' + inventory_file_name + '" ' +
    ' --list-tasks-json' +
    ' --list-hosts  ' +
    '' + vault_password_file_option;

  if(extra_vars){
    command += ' --extra-vars  \''+ JSON.stringify(extra_vars) +'\''
  }

  ssh2_exec.executeCommand(user, command, logFile, null,
    function(response){
      // Folder Exists
      completeCallback(response);
    },
    function(errorResponse){
      errorCallback(errorResponse)
    });
};


/**
 * Delete temporary playbook
 * @param user
 * @param destinationPath
 */
var deleteTempoararyPlaybook = function(user, destinationPath){
  var command = 'rm "' + destinationPath + '"';
  ssh2_exec.executeCommand(user, command, null, null,
    function(response){
      // Folder Exists
      console.log("Deleted temporary playbook - " + destinationPath)
    },
    function(errorResponse){
      console.log("Delete temporary playbook - " + destinationPath + " failed " + errorResponse)
    });
};

/**
 * Get List of Tasks, Tags and Hosts associated to a playbook
 * @param user
 * @param projectName
 * @param ansiblePlaybooks
 * @param completeCallback
 * @param errorCallback
 * @param decryptedVaultPassword
 */
exports.getAnsibleTasks = function(user, projectName, ansiblePlaybooks, completeCallback, errorCallback, decryptedVaultPassword, extra_vars){

  console.log("Get Ansible Tasks");

  var playbook_name = null;

  var projectFolder = '"' + config.scriptEngine.projectsFolder + projectName + '"';

  if(!ansiblePlaybooks)return errorCallback('No ansible type specified. Must be file name of an Ansible Playbook(s)');
  if(ansiblePlaybooks && ansiblePlaybooks.length === 1) {
    playbook_name = ansiblePlaybooks[0] + '.yml';
    _getAnsibleTasks(projectFolder, playbook_name, user, completeCallback, errorCallback, decryptedVaultPassword, extra_vars);
  }
  else {
    prepareTemporaryPlaybook(ansiblePlaybooks, projectName, user, function(playbook_name, destinationPath){
      _getAnsibleTasks(projectFolder, playbook_name, user, function(ansibleTasksResponse){
        completeCallback(ansibleTasksResponse);
        //Cleanup - Delete temporary playbook
        deleteTempoararyPlaybook(user, destinationPath)
      }, errorCallback, decryptedVaultPassword, extra_vars)
    }, errorCallback)

  }
};


/**
 * Get Rollback Points
 * @param user
 * @param projectName
 * @param completeCallback
 * @param errorCallback
 */
exports.getRollbackPoints = function(user, projectName, completeCallback, errorCallback){

  console.log("Get Rollback points");

  var playbook_name = null;

  var projectFolder = config.scriptEngine.projectsFolder + projectName;
  var destinationPath = projectFolder + "/playbooks/backup_and_restore/rollback-points.yml";

  var command = 'cat "' + destinationPath + '"';
  ssh2_exec.executeCommand(user, command, null, null,
    function(response){
      // Folder Exists
      var callbackSent = false;
      try{
        var yamlData = YAML.parse(response, function(err){
          callbackSent = true;
          errorCallback("Failed to parse rollback points " + err);
          console.log("Failed to parse rollback points " + err)
        });

        if(!callbackSent){
          if(yamlData){
            if(yamlData.rollback_points)
              completeCallback(yamlData.rollback_points);
            else
              completeCallback(null)
          }else{
            errorCallback("Could not retrieve rollback points")
          }
        }
      }
      catch(e){
        errorCallback("Could not retrieve rollback points " + e)
      }

    },
    function(errorResponse){
      errorCallback(errorResponse);
      console.log("Failed to get rollback points at " + destinationPath + " - " + errorResponse)

    });


};

/**
 * Delete Project Folder
 * @param user
 * @param projectName
 * @param completeCallback
 * @param errorCallback
 */
exports.deleteProjectFolder = function(user, projectName, completeCallback, errorCallback){
  console.log("Delete Project " + projectName);
  var projectFolder = config.scriptEngine.projectsFolder + projectName;

  var command = 'rm -r "' + projectFolder + '"';
  ssh2_exec.executeCommand(user, command, null, null,
    function(response){
      // Folder Deleted
      completeCallback();

    },
    function(errorResponse){
      errorCallback("Failed to delete project folder " + errorResponse);
      console.error("Failed to delete project folder " + errorResponse);
    });
};
