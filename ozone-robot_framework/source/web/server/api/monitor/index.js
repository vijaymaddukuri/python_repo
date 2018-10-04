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


'use strict';

var express = require('express');
var controller = require('./monitor.controller');
var authService = require('../../auth/auth.service');
var router = express.Router();

router.post('/:type', authService.isAuthenticated(), controller.health);

module.exports = router;
