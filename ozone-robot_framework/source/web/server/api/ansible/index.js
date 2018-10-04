'use strict';

var express = require('express');
var controller = require('./ansible.controller');
var authService = require('../../auth/auth.service');
var router = express.Router();

router.get('/', authService.isAuthenticated(), controller.index);
router.get('/:id/logs', authService.isAuthenticated(), controller.getLogs);
router.get('/:id',authService.isAuthenticated(), controller.show);
router.get('/total_rows', authService.isAuthenticated(), controller.totalRows);

router.put('/:id', authService.isAuthenticated(), controller.update);
router.patch('/:id',authService.isAuthenticated(), controller.update);
router.delete('/:id',authService.isAuthenticated(), controller.destroy);

router.post('/playbooks',authService.isAuthenticated(), controller.ansibleListPlaybooks);
router.post('/playbook_tasks',authService.isAuthenticated(), controller.ansibleListTasks);
router.post('/execute',authService.isAuthenticated(), controller.ansibleExecute);
router.post('/stop',authService.isAuthenticated(), controller.ansibleStop);
router.post('/kill',authService.isAuthenticated(), controller.ansibleKill);
router.post('/roll_back_points',authService.isAuthenticated(), controller.getRollbackPoints);

module.exports = router;
