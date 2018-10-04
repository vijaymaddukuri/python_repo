/**
 * Ansible model events
 */

'use strict';

import {EventEmitter} from 'events';
import Ansible from './ansible.model';
var AnsibleEvents = new EventEmitter();

// Set max event listeners (0 == unlimited)
AnsibleEvents.setMaxListeners(0);

// Model events
var events = {
  'save': 'save',
  'remove': 'remove'
};

// Register the event emitter to the model events
for (var e in events) {
  var event = events[e];
  Ansible.schema.post(e, emitEvent(event));
}

function emitEvent(event) {
  return function(doc) {
    AnsibleEvents.emit(event + ':' + doc._id, doc);
    AnsibleEvents.emit(event, doc);
  }
}

export default AnsibleEvents;
