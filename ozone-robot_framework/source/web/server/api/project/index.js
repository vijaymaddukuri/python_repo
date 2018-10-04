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
var controller = require('./project.controller');
var authService = require('../../auth/auth.service');
var router = express.Router();

router.get('/', authService.isAuthenticated(), controller.index);
router.get('/get_default_config_data', authService.isAuthenticated(), controller.getDefaultConfigData);
router.get('/decrypted_data/:id', authService.isAuthenticated(), controller.getDecryptedData);
router.get('/:id', authService.isAuthenticated(),controller.show);
router.post('/', authService.isAuthenticated(),controller.create);
router.put('/:id', authService.isAuthenticated(),controller.update);
router.patch('/:id', authService.isAuthenticated(),controller.update);
router.delete('/:id', authService.isAuthenticated(),controller.destroy);


router.post('/update_ansible_variable_files', authService.isAuthenticated(),controller.updateAnsibleVariableFiles);
router.post('/update_ansible_playbook_files', authService.isAuthenticated(),controller.updateAnsiblePlaybookFiles);

router.get('/download_input_template', controller.downloadInputTemplate);

module.exports = router;
