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

var snapshotCtrlStub = {
  index: 'snapshotCtrl.index',
  show: 'snapshotCtrl.show',
  create: 'snapshotCtrl.create',
  update: 'snapshotCtrl.update',
  destroy: 'snapshotCtrl.destroy'
};

var routerStub = {
  get: sinon.spy(),
  put: sinon.spy(),
  patch: sinon.spy(),
  post: sinon.spy(),
  delete: sinon.spy()
};

// require the index with our stubbed out modules
var snapshotIndex = proxyquire('./index.js', {
  'express': {
    Router: function() {
      return routerStub;
    }
  },
  './snapshot.controller': snapshotCtrlStub
});

describe('Snapshot API Router:', function() {

  it('should return an express router instance', function() {
    snapshotIndex.should.equal(routerStub);
  });

  describe('GET /api/snapshots', function() {

    it('should route to snapshot.controller.index', function() {
      routerStub.get
        .withArgs('/', 'snapshotCtrl.index')
        .should.have.been.calledOnce;
    });

  });

  describe('GET /api/snapshots/:id', function() {

    it('should route to snapshot.controller.show', function() {
      routerStub.get
        .withArgs('/:id', 'snapshotCtrl.show')
        .should.have.been.calledOnce;
    });

  });

  describe('POST /api/snapshots', function() {

    it('should route to snapshot.controller.create', function() {
      routerStub.post
        .withArgs('/', 'snapshotCtrl.create')
        .should.have.been.calledOnce;
    });

  });

  describe('PUT /api/snapshots/:id', function() {

    it('should route to snapshot.controller.update', function() {
      routerStub.put
        .withArgs('/:id', 'snapshotCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('PATCH /api/snapshots/:id', function() {

    it('should route to snapshot.controller.update', function() {
      routerStub.patch
        .withArgs('/:id', 'snapshotCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('DELETE /api/snapshots/:id', function() {

    it('should route to snapshot.controller.destroy', function() {
      routerStub.delete
        .withArgs('/:id', 'snapshotCtrl.destroy')
        .should.have.been.calledOnce;
    });

  });

});
