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
 * Main application routes
 * @module
 */

'use strict';

import errors from './components/errors';
import path from 'path';

/**
 * Application routes
 * @function
 * @param app
 */
export default function(app) {
  // Insert routes below
  app.use('/api/system', require('./api/system'));
  app.use('/api/ansible', require('./api/ansible'));
  app.use('/api/kue', require('./api/kue'));
  app.use('/api/logs', require('./api/log'));
  app.use('/api/upgrade', require('./api/upgrade'));
  app.use('/api/snapshots', require('./api/snapshot'));
  app.use('/api/monitor', require('./api/monitor'));
  app.use('/api/projects', require('./api/project'));
  app.use('/api/users', require('./api/user'));

  app.use('/auth', require('./auth').default);

  // All undefined asset or api routes should return a 404
  app.route('/:url(api|auth|components|app|bower_components|assets)/*')
   .get(errors[404]);

  // All other routes should redirect to the index.html
  app.route('/*')
    .get((req, res) => {
      res.sendFile(path.resolve(app.get('appPath') + '/index.html'));
    });
}

