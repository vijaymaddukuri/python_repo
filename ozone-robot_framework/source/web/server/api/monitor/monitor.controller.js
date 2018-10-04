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
 * Using Rails-like standard naming convention for endpoints.
 * GET     /api/monitor              ->  index
 * POST    /api/monitor              ->  create
 * GET     /api/monitor/:id          ->  show
 * PUT     /api/monitor/:id          ->  update
 * DELETE  /api/monitor/:id          ->  destroy
 */

'use strict';

import _ from 'lodash';
var monitortool = require('../../components/monitor/monitortool');


// Creates a new Monitor in the DB
export function health(req, res) {

  var monitorData = req.body;
  var monitorType = monitorData.type;
  var time = new Date().getTime();
  var logfilename = 'monitor_' + monitorType + '_' + req.user.name.replace(" ","_") + '_' + time + '.log';

  monitorData.commandType = req.params.type; //health, version, license etc

  monitortool.monitor(req.user.name,monitorData,logfilename,
    function(data){
      //res.send(data)
      //data Callback
      res.write(data)
    },
    function(data){
      //res.send(data)
      //Complete Callback
      res.end(data)
    },
    function(error){
      //res.status(500).send(error);
      res.status(500);
      res.send(error);

    });

  /*return Monitor.create(req.body)
    .then(respondWithResult(res, 201))
    .catch(handleError(res));*/
}
