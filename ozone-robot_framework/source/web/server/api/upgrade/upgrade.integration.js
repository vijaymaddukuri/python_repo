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

var app = require('../..');
import request from 'supertest';

var newUpgrade;

describe('Upgrade API:', function() {

  describe('GET /api/upgrade', function() {
    var upgrades;

    beforeEach(function(done) {
      request(app)
        .get('/api/upgrade')
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          upgrades = res.body;
          done();
        });
    });

    it('should respond with JSON array', function() {
      upgrades.should.be.instanceOf(Array);
    });

  });

  describe('POST /api/upgrade', function() {
    beforeEach(function(done) {
      request(app)
        .post('/api/upgrade')
        .send({
          name: 'New Upgrade',
          info: 'This is the brand new upgrade!!!'
        })
        .expect(201)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          newUpgrade = res.body;
          done();
        });
    });

    it('should respond with the newly created upgrade', function() {
      newUpgrade.name.should.equal('New Upgrade');
      newUpgrade.info.should.equal('This is the brand new upgrade!!!');
    });

  });

  describe('GET /api/upgrade/:id', function() {
    var upgrade;

    beforeEach(function(done) {
      request(app)
        .get('/api/upgrade/' + newUpgrade._id)
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          upgrade = res.body;
          done();
        });
    });

    afterEach(function() {
      upgrade = {};
    });

    it('should respond with the requested upgrade', function() {
      upgrade.name.should.equal('New Upgrade');
      upgrade.info.should.equal('This is the brand new upgrade!!!');
    });

  });

  describe('PUT /api/upgrade/:id', function() {
    var updatedUpgrade;

    beforeEach(function(done) {
      request(app)
        .put('/api/upgrade/' + newUpgrade._id)
        .send({
          name: 'Updated Upgrade',
          info: 'This is the updated upgrade!!!'
        })
        .expect(200)
        .expect('Content-Type', /json/)
        .end(function(err, res) {
          if (err) {
            return done(err);
          }
          updatedUpgrade = res.body;
          done();
        });
    });

    afterEach(function() {
      updatedUpgrade = {};
    });

    it('should respond with the updated upgrade', function() {
      updatedUpgrade.name.should.equal('Updated Upgrade');
      updatedUpgrade.info.should.equal('This is the updated upgrade!!!');
    });

  });

  describe('DELETE /api/upgrade/:id', function() {

    it('should respond with 204 on successful removal', function(done) {
      request(app)
        .delete('/api/upgrade/' + newUpgrade._id)
        .expect(204)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          done();
        });
    });

    it('should respond with 404 when upgrade does not exist', function(done) {
      request(app)
        .delete('/api/upgrade/' + newUpgrade._id)
        .expect(404)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          done();
        });
    });

  });

});
