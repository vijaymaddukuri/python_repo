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


var nodemailer = require('nodemailer');
var smtpTransport = require('nodemailer-smtp-transport');

var logger = require('../Logger');
var serverLogger = logger.serverLogger;

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

import appconfig from '../../config/environment';

// create reusable transporter object using SMTP transport
var transporter = nodemailer.createTransport(smtpTransport({
    host: appconfig.email.smtpServer,
    port: appconfig.email.smtpServerPort
}));

// NB! No need to recreate the transporter object. You can use
// the same transporter object for all e-mails


exports.emailAdmins = function(subject, messageBody){
  if(appconfig.email.disabled){
    serverLogger.info("Not sending email as email is disabled in config file.");
    return
  }
	// setup e-mail data with unicode symbols
	console.log("Here");
	var mailOptions = {
	    from: appconfig.email.from_email, // sender address
	    to: appconfig.email.email_admins, // list of receivers
	    subject: subject, // Subject line
	    text: messageBody, // plaintext body
	    html: messageBody // html body
	};

	serverLogger.info("Sending Email " + subject);

	// send mail with defined transport object
	transporter.sendMail(mailOptions, function(error, info){
	    if(error){
	    	serverLogger.error("Email sent failed " + error);
	    }else{
	    	serverLogger.info('Email Success = Message sent: ' + info.response + ' Subject=' + subject);
	    }
	});
};

exports.emailAdminsWithUserInfo = function(user, subject, messageBody){
  if(appconfig.email.disabled){
    serverLogger.info("Not sending email as email is disabled in config file.");
    return
  }

  // Placeholder

};


exports.emailUser = function(user_email, subject, messageBody){
	// setup e-mail data with unicode symbols
	var mailOptions = {
	    from: appconfig.email.from_email, // sender address
	    to: user_email, // list of receivers
	    bcc: appconfig.email.email_admins,
	    subject: subject, // Subject line
	    text: messageBody, // plaintext body
	    html: messageBody // html body
	};

	serverLogger.info("Sending Email " + subject);

  if(appconfig.email.disabled){
    serverLogger.info("Not sending email as email is disabled in config file.");
    return
  }

	// send mail with defined transport object
	transporter.sendMail(mailOptions, function(error, info){
	    if(error){
	    	serverLogger.error("Email sent failed " + error);
	    }else{
	    	serverLogger.info('Email Success = Message sent: ' + info.response + ' Subject=' + subject);
	    }
	});
};
