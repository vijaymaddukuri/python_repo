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

var newMonitor;

describe('Monitor API:', function() {

  describe('GET /api/monitor', function() {
    var monitors;

    beforeEach(function(done) {
      request(app)
        .get('/api/monitor')
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          monitors = res.body;
          done();
        });
    });

    it('should respond with JSON array', function() {
      monitors.should.be.instanceOf(Array);
    });

  });

  describe('POST /api/monitor', function() {
    beforeEach(function(done) {
      request(app)
        .post('/api/monitor')
        .send({
          name: 'New Monitor',
          info: 'This is the brand new monitor!!!'
        })
        .expect(201)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          newMonitor = res.body;
          done();
        });
    });

    it('should respond with the newly created monitor', function() {
      newMonitor.name.should.equal('New Monitor');
      newMonitor.info.should.equal('This is the brand new monitor!!!');
    });

  });

  describe('GET /api/monitor/:id', function() {
    var monitor;

    beforeEach(function(done) {
      request(app)
        .get('/api/monitor/' + newMonitor._id)
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          monitor = res.body;
          done();
        });
    });

    afterEach(function() {
      monitor = {};
    });

    it('should respond with the requested monitor', function() {
      monitor.name.should.equal('New Monitor');
      monitor.info.should.equal('This is the brand new monitor!!!');
    });

  });

  describe('PUT /api/monitor/:id', function() {
    var updatedMonitor;

    beforeEach(function(done) {
      request(app)
        .put('/api/monitor/' + newMonitor._id)
        .send({
          name: 'Updated Monitor',
          info: 'This is the updated monitor!!!'
        })
        .expect(200)
        .expect('Content-Type', /json/)
        .end(function(err, res) {
          if (err) {
            return done(err);
          }
          updatedMonitor = res.body;
          done();
        });
    });

    afterEach(function() {
      updatedMonitor = {};
    });

    it('should respond with the updated monitor', function() {
      updatedMonitor.name.should.equal('Updated Monitor');
      updatedMonitor.info.should.equal('This is the updated monitor!!!');
    });

  });

  describe('DELETE /api/monitor/:id', function() {

    it('should respond with 204 on successful removal', function(done) {
      request(app)
        .delete('/api/monitor/' + newMonitor._id)
        .expect(204)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          done();
        });
    });

    it('should respond with 404 when monitor does not exist', function(done) {
      request(app)
        .delete('/api/monitor/' + newMonitor._id)
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
