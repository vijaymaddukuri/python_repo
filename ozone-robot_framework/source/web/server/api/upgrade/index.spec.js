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

var upgradeCtrlStub = {
  index: 'upgradeCtrl.index',
  show: 'upgradeCtrl.show',
  create: 'upgradeCtrl.create',
  update: 'upgradeCtrl.update',
  destroy: 'upgradeCtrl.destroy'
};

var routerStub = {
  get: sinon.spy(),
  put: sinon.spy(),
  patch: sinon.spy(),
  post: sinon.spy(),
  delete: sinon.spy()
};

// require the index with our stubbed out modules
var upgradeIndex = proxyquire('./index.js', {
  'express': {
    Router: function() {
      return routerStub;
    }
  },
  './upgrade.controller': upgradeCtrlStub
});

describe('Upgrade API Router:', function() {

  it('should return an express router instance', function() {
    upgradeIndex.should.equal(routerStub);
  });

  describe('GET /api/upgrade', function() {

    it('should route to upgrade.controller.index', function() {
      routerStub.get
        .withArgs('/', 'upgradeCtrl.index')
        .should.have.been.calledOnce;
    });

  });

  describe('GET /api/upgrade/:id', function() {

    it('should route to upgrade.controller.show', function() {
      routerStub.get
        .withArgs('/:id', 'upgradeCtrl.show')
        .should.have.been.calledOnce;
    });

  });

  describe('POST /api/upgrade', function() {

    it('should route to upgrade.controller.create', function() {
      routerStub.post
        .withArgs('/', 'upgradeCtrl.create')
        .should.have.been.calledOnce;
    });

  });

  describe('PUT /api/upgrade/:id', function() {

    it('should route to upgrade.controller.update', function() {
      routerStub.put
        .withArgs('/:id', 'upgradeCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('PATCH /api/upgrade/:id', function() {

    it('should route to upgrade.controller.update', function() {
      routerStub.patch
        .withArgs('/:id', 'upgradeCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('DELETE /api/upgrade/:id', function() {

    it('should route to upgrade.controller.destroy', function() {
      routerStub.delete
        .withArgs('/:id', 'upgradeCtrl.destroy')
        .should.have.been.calledOnce;
    });

  });

});
