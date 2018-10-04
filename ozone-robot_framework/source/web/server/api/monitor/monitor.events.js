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
 * Monitor model events
 */

'use strict';

import {EventEmitter} from 'events';
import Monitor from './monitor.model';
var MonitorEvents = new EventEmitter();

// Set max event listeners (0 == unlimited)
MonitorEvents.setMaxListeners(0);

// Model events
var events = {
  'save': 'save',
  'remove': 'remove'
};

// Register the event emitter to the model events
for (var e in events) {
  var event = events[e];
  Monitor.schema.post(e, emitEvent(event));
}

function emitEvent(event) {
  return function(doc) {
    MonitorEvents.emit(event + ':' + doc._id, doc);
    MonitorEvents.emit(event, doc);
  }
}

export default MonitorEvents;
