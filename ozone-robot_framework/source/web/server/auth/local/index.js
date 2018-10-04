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

import express from 'express';
import passport from 'passport';
import {signToken} from '../auth.service';
var emailer = require('../../components/email/email_smtp.js');
var router = express.Router();
var logger = require('../../components/Logger').authLogger;

router.post('/', function(req, res, next) {

  passport.authenticate('local', function(err, user, info) {
    console.log("User = " + user)
    var error = err || info;
    if (error) {
      return res.status(401).json(error);
    }
    if (!user) {
      return res.status(404).json({message: 'Something went wrong, please try again.'});
    }
    var userDoc = JSON.parse(JSON.stringify(user[0]));
    var token = signToken(userDoc._id, user.role);
    res.json({ token });
    //if(user.ntid !== 'mannam4'){
      emailer.emailAdminsWithUserInfo(userDoc.email, "User Logged in", "");
    //}
    logger.info("User - " + (userDoc.email || user.ntid)+ " Logged in");

  })(req, res, next)
});

export default router;
