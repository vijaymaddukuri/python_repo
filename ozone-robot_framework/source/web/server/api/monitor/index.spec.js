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

var monitorCtrlStub = {
  index: 'monitorCtrl.index',
  show: 'monitorCtrl.show',
  create: 'monitorCtrl.create',
  update: 'monitorCtrl.update',
  destroy: 'monitorCtrl.destroy'
};

var routerStub = {
  get: sinon.spy(),
  put: sinon.spy(),
  patch: sinon.spy(),
  post: sinon.spy(),
  delete: sinon.spy()
};

// require the index with our stubbed out modules
var monitorIndex = proxyquire('./index.js', {
  'express': {
    Router: function() {
      return routerStub;
    }
  },
  './monitor.controller': monitorCtrlStub
});

describe('Monitor API Router:', function() {

  it('should return an express router instance', function() {
    monitorIndex.should.equal(routerStub);
  });

  describe('GET /api/monitor', function() {

    it('should route to monitor.controller.index', function() {
      routerStub.get
        .withArgs('/', 'monitorCtrl.index')
        .should.have.been.calledOnce;
    });

  });

  describe('GET /api/monitor/:id', function() {

    it('should route to monitor.controller.show', function() {
      routerStub.get
        .withArgs('/:id', 'monitorCtrl.show')
        .should.have.been.calledOnce;
    });

  });

  describe('POST /api/monitor', function() {

    it('should route to monitor.controller.create', function() {
      routerStub.post
        .withArgs('/', 'monitorCtrl.create')
        .should.have.been.calledOnce;
    });

  });

  describe('PUT /api/monitor/:id', function() {

    it('should route to monitor.controller.update', function() {
      routerStub.put
        .withArgs('/:id', 'monitorCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('PATCH /api/monitor/:id', function() {

    it('should route to monitor.controller.update', function() {
      routerStub.patch
        .withArgs('/:id', 'monitorCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('DELETE /api/monitor/:id', function() {

    it('should route to monitor.controller.destroy', function() {
      routerStub.delete
        .withArgs('/:id', 'monitorCtrl.destroy')
        .should.have.been.calledOnce;
    });

  });

});
