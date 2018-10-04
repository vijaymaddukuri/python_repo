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

var newSnapshot;

describe('Snapshot API:', function() {

  describe('GET /api/snapshots', function() {
    var snapshots;

    beforeEach(function(done) {
      request(app)
        .get('/api/snapshots')
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          snapshots = res.body;
          done();
        });
    });

    it('should respond with JSON array', function() {
      snapshots.should.be.instanceOf(Array);
    });

  });

  describe('POST /api/snapshots', function() {
    beforeEach(function(done) {
      request(app)
        .post('/api/snapshots')
        .send({
          name: 'New Snapshot',
          info: 'This is the brand new snapshot!!!'
        })
        .expect(201)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          newSnapshot = res.body;
          done();
        });
    });

    it('should respond with the newly created snapshot', function() {
      newSnapshot.name.should.equal('New Snapshot');
      newSnapshot.info.should.equal('This is the brand new snapshot!!!');
    });

  });

  describe('GET /api/snapshots/:id', function() {
    var snapshot;

    beforeEach(function(done) {
      request(app)
        .get('/api/snapshots/' + newSnapshot._id)
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          snapshot = res.body;
          done();
        });
    });

    afterEach(function() {
      snapshot = {};
    });

    it('should respond with the requested snapshot', function() {
      snapshot.name.should.equal('New Snapshot');
      snapshot.info.should.equal('This is the brand new snapshot!!!');
    });

  });

  describe('PUT /api/snapshots/:id', function() {
    var updatedSnapshot;

    beforeEach(function(done) {
      request(app)
        .put('/api/snapshots/' + newSnapshot._id)
        .send({
          name: 'Updated Snapshot',
          info: 'This is the updated snapshot!!!'
        })
        .expect(200)
        .expect('Content-Type', /json/)
        .end(function(err, res) {
          if (err) {
            return done(err);
          }
          updatedSnapshot = res.body;
          done();
        });
    });

    afterEach(function() {
      updatedSnapshot = {};
    });

    it('should respond with the updated snapshot', function() {
      updatedSnapshot.name.should.equal('Updated Snapshot');
      updatedSnapshot.info.should.equal('This is the updated snapshot!!!');
    });

  });

  describe('DELETE /api/snapshots/:id', function() {

    it('should respond with 204 on successful removal', function(done) {
      request(app)
        .delete('/api/snapshots/' + newSnapshot._id)
        .expect(204)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          done();
        });
    });

    it('should respond with 404 when snapshot does not exist', function(done) {
      request(app)
        .delete('/api/snapshots/' + newSnapshot._id)
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
