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

var proxyquire = require('proxyquire').noPreserveCache();

var kueCtrlStub = {
  index: 'kueCtrl.index',
  show: 'kueCtrl.show',
  create: 'kueCtrl.create',
  update: 'kueCtrl.update',
  destroy: 'kueCtrl.destroy'
};

var routerStub = {
  get: sinon.spy(),
  put: sinon.spy(),
  patch: sinon.spy(),
  post: sinon.spy(),
  delete: sinon.spy()
};

// require the index with our stubbed out modules
var kueIndex = proxyquire('./index.js', {
  'express': {
    Router: function() {
      return routerStub;
    }
  },
  './kue.controller': kueCtrlStub
});

describe('Kue API Router:', function() {

  it('should return an express router instance', function() {
    kueIndex.should.equal(routerStub);
  });

  describe('GET /api/kue', function() {

    it('should route to kue.controller.index', function() {
      routerStub.get
        .withArgs('/', 'kueCtrl.index')
        .should.have.been.calledOnce;
    });

  });

  describe('GET /api/kue/:id', function() {

    it('should route to kue.controller.show', function() {
      routerStub.get
        .withArgs('/:id', 'kueCtrl.show')
        .should.have.been.calledOnce;
    });

  });

  describe('POST /api/kue', function() {

    it('should route to kue.controller.create', function() {
      routerStub.post
        .withArgs('/', 'kueCtrl.create')
        .should.have.been.calledOnce;
    });

  });

  describe('PUT /api/kue/:id', function() {

    it('should route to kue.controller.update', function() {
      routerStub.put
        .withArgs('/:id', 'kueCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('PATCH /api/kue/:id', function() {

    it('should route to kue.controller.update', function() {
      routerStub.patch
        .withArgs('/:id', 'kueCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('DELETE /api/kue/:id', function() {

    it('should route to kue.controller.destroy', function() {
      routerStub.delete
        .withArgs('/:id', 'kueCtrl.destroy')
        .should.have.been.calledOnce;
    });

  });

});
