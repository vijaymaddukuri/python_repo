'use strict';

var app = require('../..');
import request from 'supertest';

var newSystem;

describe('System API:', function() {

  describe('GET /api/systems', function() {
    var systems;

    beforeEach(function(done) {
      request(app)
        .get('/api/systems')
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          systems = res.body;
          done();
        });
    });

    it('should respond with JSON array', function() {
      systems.should.be.instanceOf(Array);
    });

  });

  describe('POST /api/systems', function() {
    beforeEach(function(done) {
      request(app)
        .post('/api/systems')
        .send({
          name: 'New System',
          info: 'This is the brand new system!!!'
        })
        .expect(201)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          newSystem = res.body;
          done();
        });
    });

    it('should respond with the newly created system', function() {
      newSystem.name.should.equal('New System');
      newSystem.info.should.equal('This is the brand new system!!!');
    });

  });

  describe('GET /api/systems/:id', function() {
    var system;

    beforeEach(function(done) {
      request(app)
        .get('/api/systems/' + newSystem._id)
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          system = res.body;
          done();
        });
    });

    afterEach(function() {
      system = {};
    });

    it('should respond with the requested system', function() {
      system.name.should.equal('New System');
      system.info.should.equal('This is the brand new system!!!');
    });

  });

  describe('PUT /api/systems/:id', function() {
    var updatedSystem;

    beforeEach(function(done) {
      request(app)
        .put('/api/systems/' + newSystem._id)
        .send({
          name: 'Updated System',
          info: 'This is the updated system!!!'
        })
        .expect(200)
        .expect('Content-Type', /json/)
        .end(function(err, res) {
          if (err) {
            return done(err);
          }
          updatedSystem = res.body;
          done();
        });
    });

    afterEach(function() {
      updatedSystem = {};
    });

    it('should respond with the updated system', function() {
      updatedSystem.name.should.equal('Updated System');
      updatedSystem.info.should.equal('This is the updated system!!!');
    });

  });

  describe('DELETE /api/systems/:id', function() {

    it('should respond with 204 on successful removal', function(done) {
      request(app)
        .delete('/api/systems/' + newSystem._id)
        .expect(204)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          done();
        });
    });

    it('should respond with 404 when system does not exist', function(done) {
      request(app)
        .delete('/api/systems/' + newSystem._id)
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
