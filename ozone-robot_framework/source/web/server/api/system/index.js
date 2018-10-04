'use strict';

var express = require('express');
var controller = require('./system.controller');
var authService = require('../../auth/auth.service');
var router = express.Router();

router.post('/services/start', controller.startServices);

router.get('/agent',  authService.isAuthenticated(), controller.agent);
router.get('/services',  authService.isAuthenticated(), controller.services);
router.get('/queue/jobs',  authService.isAuthenticated(), controller.queueJobs);

router.post('/queue/requeue',  authService.isAuthenticated(), controller.requeue);
router.post('/queue/cleanup',  authService.isAuthenticated(), controller.cleanupQueue);

router.get('/password/isset',  authService.isAuthenticated(), controller.masterPassword);
router.post('/password',  authService.isAuthenticated(), controller.setMasterPassword);

module.exports = router;
