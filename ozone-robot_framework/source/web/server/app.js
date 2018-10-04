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
 * Main application file
 * @module
 */

'use strict';

import express from 'express';
/*
import mongoose from 'mongoose';
mongoose.Promise = require('bluebird');
*/
import config from './config/environment';
import http from 'http';
var bodyParser = require('body-parser');
var NodeCache = require( "node-cache" );

/*// Connect to MongoDB
mongoose.connect(config.mongo.uri, config.mongo.options);
mongoose.connection.on('error', function(err) {
  console.error('MongoDB connection error: ' + err);
  process.exit(-1);
});*/

// Populate databases with sample data
if (config.seedDB) { require('./config/seed'); }

// Setup server
var app = express();
app.use(bodyParser.json({limit:'50mb'}));
var server = http.createServer(app);
require('./config/express').default(app);
require('./routes').default(app);

// Initialize Servercache
global.serverCache = new NodeCache();

// Start server
function startServer() {
  app.angularFullstack = server.listen(config.port, config.ip, function() {
    console.log('Express server listening on %d, in %s mode', config.port, app.get('env'));
  });

}

setImmediate(startServer);

// Expose app
exports = module.exports = app;
