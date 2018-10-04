'use strict';

import mongoose from 'mongoose';

var SystemSchema = new mongoose.Schema({
  name: String,
  info: String,
  active: Boolean
});

export default mongoose.model('System', SystemSchema);
