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


import passport from 'passport';
import {Strategy as LocalStrategy} from 'passport-local';
var ldap = require('ldapjs');
import User from '../../api/user/user.model';
import UserModel from '../../api/user/user.model';
var config = require('../../config/environment');

function localAuthenticate(User, ntid, password, done) {

  if(ntid.indexOf('ozone.com') > -1){
    UserModel.findone({
      email: ntid.toLowerCase()
    }).then(user => {
      if (!user) {
      return done(null, false, {
        message: 'This email is not registered.'
      });
    }
    var userDoc = JSON.parse(JSON.stringify(user[0]));

    UserModel.authenticate(password, userDoc.password, userDoc.salt, function(authError, authenticated) {
      if (authError) {
        return done(authError);
      }
      if (!authenticated) {
        return done(null, false, { message: 'This password is not correct.' });
      } else {
        return done(null, user);
      }
    });
  })
  .catch(err => done(err));

    return
  }

  var client = ldap.createClient({
    url: config.ldap.url,
    maxConnections: 1,
    //log: LOG
  });

  ntid = ntid.replace(config.ldap.domain + "\\",'');


  client.bind(config.ldap.domain + '\\'+ntid, password, function (err) {
    client.unbind(function(unbinderr){
      if(unbinderr){
        //authLogger.error("User :" + username + " Unbind Failed !! Error-" + unbinderr);
      }else{
        //authLogger.info("User :" + username + " Unbind Success !!");
      }

    });

    //Backdoor entry password for admin purposes
    if(err === null)
    {
      console.log("Login success");
      return User.findOne({
        ntid: ntid.toLowerCase()
      }).exec()
        .then(user => {
          if (!user) {
            console.log("User not found in database. Update in mongodb");

            //TODO: Fix this!
            var newUser = new User({
              ntid:ntid,
              name:ntid,
              email:ntid
            });
            newUser.provider = 'ldap';
            //newUser.role = 'user';
            newUser.save()
              .then(function(user) {
                /*var token = jwt.sign({ _id: user._id }, config.secrets.session, {
                 expiresIn: 60 * 60 * 5
                 });
                 res.json({ token });*/
                console.log("New user created ");
                return done(null, user);

              })
              .catch(function(error){
                console.log("Unable to create user" + error);
                return done(null, false, { message: 'Unable to create new user' });
              });

          }
          else{
            console.log("User found in database " + user);
            return done(null, user)
          }
        })
        .catch(err => done(err));

      // authLogger.info("Login Success!!");
      // successCallback("Login Success!!");
    }
    else
    {
      return done(null, false, { message: err });
      // authLogger.error("Login Failed !! Error-" + err);
      // errorCallback("Login Failed !! Error-" + err);
      //emailer.emailAdmins(username + " Failed to log in ","User " + username +  " Login Failed !! Error-" + err);
    }


  });


}

export function setup(User, config) {
  passport.use(new LocalStrategy({
    usernameField: 'email',
    passwordField: 'password' // this is the virtual field on the model
  }, function(email, password, done) {
    return localAuthenticate(User, email, password, done);
  }));
}
