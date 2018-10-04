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

import {Router} from 'express';
import * as controller from './user.controller';
import * as auth from '../../auth/auth.service';

var router = new Router();

router.get('/', auth.hasRole('admin'), controller.index);
router.delete('/:id', auth.hasRole('admin'), controller.destroy);
router.put('/:id', auth.hasRole('admin'), controller.update);
router.get('/me', auth.isAuthenticated(), controller.me);
router.get('/ehcdefaultusers', auth.isAuthenticated(), controller.ehcDefaultUsers);
router.put('/:id/password', auth.isAuthenticated(), controller.changePassword);

router.get('/:id', auth.isAuthenticated(), controller.show);
router.post('/', controller.create);
router.post('/email', auth.isAuthenticated(), controller.email);

module.exports = router;
