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

var newKue;

describe('Kue API:', function() {

  describe('GET /api/kue', function() {
    var kues;

    beforeEach(function(done) {
      request(app)
        .get('/api/kue')
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          kues = res.body;
          done();
        });
    });

    it('should respond with JSON array', function() {
      kues.should.be.instanceOf(Array);
    });

  });

  describe('POST /api/kue', function() {
    beforeEach(function(done) {
      request(app)
        .post('/api/kue')
        .send({
          name: 'New Kue',
          info: 'This is the brand new kue!!!'
        })
        .expect(201)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          newKue = res.body;
          done();
        });
    });

    it('should respond with the newly created kue', function() {
      newKue.name.should.equal('New Kue');
      newKue.info.should.equal('This is the brand new kue!!!');
    });

  });

  describe('GET /api/kue/:id', function() {
    var kue;

    beforeEach(function(done) {
      request(app)
        .get('/api/kue/' + newKue._id)
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          kue = res.body;
          done();
        });
    });

    afterEach(function() {
      kue = {};
    });

    it('should respond with the requested kue', function() {
      kue.name.should.equal('New Kue');
      kue.info.should.equal('This is the brand new kue!!!');
    });

  });

  describe('PUT /api/kue/:id', function() {
    var updatedKue;

    beforeEach(function(done) {
      request(app)
        .put('/api/kue/' + newKue._id)
        .send({
          name: 'Updated Kue',
          info: 'This is the updated kue!!!'
        })
        .expect(200)
        .expect('Content-Type', /json/)
        .end(function(err, res) {
          if (err) {
            return done(err);
          }
          updatedKue = res.body;
          done();
        });
    });

    afterEach(function() {
      updatedKue = {};
    });

    it('should respond with the updated kue', function() {
      updatedKue.name.should.equal('Updated Kue');
      updatedKue.info.should.equal('This is the updated kue!!!');
    });

  });

  describe('DELETE /api/kue/:id', function() {

    it('should respond with 204 on successful removal', function(done) {
      request(app)
        .delete('/api/kue/' + newKue._id)
        .expect(204)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          done();
        });
    });

    it('should respond with 404 when kue does not exist', function(done) {
      request(app)
        .delete('/api/kue/' + newKue._id)
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
