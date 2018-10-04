'use strict';

var app = require('../..');
import request from 'supertest';

var newAnsible;

describe('Ansible API:', function() {

  describe('GET /api/ansible', function() {
    var ansibles;

    beforeEach(function(done) {
      request(app)
        .get('/api/ansible')
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          ansibles = res.body;
          done();
        });
    });

    it('should respond with JSON array', function() {
      ansibles.should.be.instanceOf(Array);
    });

  });

  describe('POST /api/ansible', function() {
    beforeEach(function(done) {
      request(app)
        .post('/api/ansible')
        .send({
          name: 'New Ansible',
          info: 'This is the brand new ansible!!!'
        })
        .expect(201)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          newAnsible = res.body;
          done();
        });
    });

    it('should respond with the newly created ansible', function() {
      newAnsible.name.should.equal('New Ansible');
      newAnsible.info.should.equal('This is the brand new ansible!!!');
    });

  });

  describe('GET /api/ansible/:id', function() {
    var ansible;

    beforeEach(function(done) {
      request(app)
        .get('/api/ansible/' + newAnsible._id)
        .expect(200)
        .expect('Content-Type', /json/)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          ansible = res.body;
          done();
        });
    });

    afterEach(function() {
      ansible = {};
    });

    it('should respond with the requested ansible', function() {
      ansible.name.should.equal('New Ansible');
      ansible.info.should.equal('This is the brand new ansible!!!');
    });

  });

  describe('PUT /api/ansible/:id', function() {
    var updatedAnsible;

    beforeEach(function(done) {
      request(app)
        .put('/api/ansible/' + newAnsible._id)
        .send({
          name: 'Updated Ansible',
          info: 'This is the updated ansible!!!'
        })
        .expect(200)
        .expect('Content-Type', /json/)
        .end(function(err, res) {
          if (err) {
            return done(err);
          }
          updatedAnsible = res.body;
          done();
        });
    });

    afterEach(function() {
      updatedAnsible = {};
    });

    it('should respond with the updated ansible', function() {
      updatedAnsible.name.should.equal('Updated Ansible');
      updatedAnsible.info.should.equal('This is the updated ansible!!!');
    });

  });

  describe('DELETE /api/ansible/:id', function() {

    it('should respond with 204 on successful removal', function(done) {
      request(app)
        .delete('/api/ansible/' + newAnsible._id)
        .expect(204)
        .end((err, res) => {
          if (err) {
            return done(err);
          }
          done();
        });
    });

    it('should respond with 404 when ansible does not exist', function(done) {
      request(app)
        .delete('/api/ansible/' + newAnsible._id)
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
