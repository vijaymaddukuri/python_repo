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
var controller = require('./upgrade.controller');
var authService = require('../../auth/auth.service');
var router = express.Router();

router.get('/', authService.hasRole('admin'), controller.index);
router.get('/logs/:id', authService.hasRole('admin'), controller.getLogs);
router.get('/check_updates', authService.hasRole('admin'), controller.checkUpdates);
router.get('/:id', authService.hasRole('admin'), controller.show);
router.post('/', authService.hasRole('admin'), controller.create);
router.put('/:id', authService.hasRole('admin'), controller.update);
router.patch('/:id', authService.hasRole('admin'), controller.update);
router.delete('/:id', authService.hasRole('admin'), controller.destroy);

module.exports = router;
