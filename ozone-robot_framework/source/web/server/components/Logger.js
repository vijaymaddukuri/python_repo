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
 * New node file
 */

var winston = require('winston');

exports.authLogger = new winston.Logger({
    transports: [
        new winston.transports.File({
            //level: 'info',
            filename: 'logs/auth-svc.log',
            handleExceptions: false,
            json: false,
            maxsize: 5242880, //5MB
            maxFiles: 5,
            zippedArchive: true,
            colorize: false
        }),
        new winston.transports.Console({
            //level: 'debug',
            handleExceptions: false,
            //json: false,
            colorize: true
        })
    ],
    exitOnError: false
});

exports.serverLogger = new winston.Logger({
    transports: [
        new winston.transports.File({
            level: 'debug',
            filename: 'logs/server.log',
            handleExceptions: true,
            json: false,
            maxsize: 5242880, //5MB
            maxFiles: 5,
            zippedArchive: true,
            colorize: false
        })
        /*new winston.transports.Console({
            //level: 'debug',
            handleExceptions: false,
            //json: false,
            colorize: true
        })*/
    ],
    exitOnError: false
});


exports.dbLogger = new winston.Logger({
    transports: [
        new winston.transports.File({
            //level: 'info',
            filename: 'logs/db.log',
            handleExceptions: false,
            json: false,
            maxsize: 5242880, //5MB
            maxFiles: 5,
            zippedArchive: true,
            colorize: false
        })/*,
        new winston.transports.Console({
            //level: 'debug',
            handleExceptions: false,
            //json: false,
            colorize: true
        })*/
    ],
    exitOnError: false
});


exports.miscLogger = new winston.Logger({
    transports: [
        new winston.transports.File({
            //level: 'info',
            filename: 'logs/misc.log',
            handleExceptions: true,
            json: false,
            maxsize: 5242880, //5MB
            maxFiles: 5,
            zippedArchive: true,
            colorize: false
        }),
        new winston.transports.Console({
            //level: 'debug',
            handleExceptions: true,
            //json: false,
            colorize: true
        })
    ],
    exitOnError: false
});


exports.customLogger = function(logPath){

  var transports = [
    /*new winston.transports.File({
      level: 'debug',
      filename: 'logs/server.log',
      handleExceptions: true,
      json: false,
      maxsize: 5242880, //5MB
      maxFiles: 5,
      zippedArchive: true,
      colorize: false,
      name: 'server_log'
    }),*/
    /*new winston.transports.Console({
      //level: 'debug',
      handleExceptions: true,
      //json: false,
      colorize: false
    })*/
  ];

  if(logPath){
    transports.push(new winston.transports.File({
      //level: 'info',
      filename: logPath,
      handleExceptions: true,
      json: false,
      maxsize: 5242880, //5MB
      maxFiles: 100,
      zippedArchive: false,
      colorize: false,
      name: 'custom_file_path'
    }))
  }

  return new winston.Logger({
    transports: transports,
    exitOnError: false
  });

};


exports.plainLogger = function(logPath){

  var transports = [
    /*new winston.transports.File({
     //level: 'info',
     filename: logPath,
     handleExceptions: true,
     json: false,
     maxsize: 5242880, //5MB
     maxFiles: 100,
     zippedArchive: false,
     colorize: false,
     formatter: function(options) {
     // Return string will be passed to logger.
     return options.message;
     }
     }),*/
    /*new winston.transports.File({
      level: 'debug',
      filename: 'logs/server.log',
      handleExceptions: true,
      json: false,
      maxsize: 5242880, //5MB
      maxFiles: 5,
      zippedArchive: true,
      colorize: false,
      name: 'server_path'
    }),*/
    new winston.transports.Console({
      //level: 'debug',
      handleExceptions: true,
      //json: false,
      colorize: false,
      formatter: function(options) {
        // Return string will be passed to logger.
        return options.message;
      }
    })
  ];

  if(logPath){
    transports.push(new winston.transports.File({
      //level: 'info',
      filename: logPath,
      handleExceptions: true,
      json: false,
      maxsize: 5242880, //5MB
      maxFiles: 100,
      zippedArchive: false,
      colorize: false,
      formatter: function(options) {
        // Return string will be passed to logger.
        return options.message;
      },
      name: 'custom_log_path'
    }))
  }

  return new winston.Logger({
    transports: transports,
    exitOnError: false
  });

};

/*
exports.debugLogger = new winston.Logger({
    transports: [
                 new winston.transports.Console({
                     level: 'debug',
                     handleExceptions: true,
                     //json: false,
                     colorize: true
                 })
             ],
             exitOnError: false
});*/

