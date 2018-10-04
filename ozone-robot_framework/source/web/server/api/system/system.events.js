/**
 * System model events
 */

'use strict';

import {EventEmitter} from 'events';
import System from './system.model';
var SystemEvents = new EventEmitter();

// Set max event listeners (0 == unlimited)
SystemEvents.setMaxListeners(0);

// Model events
var events = {
  'save': 'save',
  'remove': 'remove'
};

// Register the event emitter to the model events
for (var e in events) {
  var event = events[e];
  System.schema.post(e, emitEvent(event));
}

function emitEvent(event) {
  return function(doc) {
    SystemEvents.emit(event + ':' + doc._id, doc);
    SystemEvents.emit(event, doc);
  }
}

export default SystemEvents;
