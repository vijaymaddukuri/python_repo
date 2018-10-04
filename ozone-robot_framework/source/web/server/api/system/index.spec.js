'use strict';

var proxyquire = require('proxyquire').noPreserveCache();

var systemCtrlStub = {
  index: 'systemCtrl.index',
  show: 'systemCtrl.show',
  create: 'systemCtrl.create',
  update: 'systemCtrl.update',
  destroy: 'systemCtrl.destroy'
};

var routerStub = {
  get: sinon.spy(),
  put: sinon.spy(),
  patch: sinon.spy(),
  post: sinon.spy(),
  delete: sinon.spy()
};

// require the index with our stubbed out modules
var systemIndex = proxyquire('./index.js', {
  'express': {
    Router: function() {
      return routerStub;
    }
  },
  './system.controller': systemCtrlStub
});

describe('System API Router:', function() {

  it('should return an express router instance', function() {
    systemIndex.should.equal(routerStub);
  });

  describe('GET /api/systems', function() {

    it('should route to system.controller.index', function() {
      routerStub.get
        .withArgs('/', 'systemCtrl.index')
        .should.have.been.calledOnce;
    });

  });

  describe('GET /api/systems/:id', function() {

    it('should route to system.controller.show', function() {
      routerStub.get
        .withArgs('/:id', 'systemCtrl.show')
        .should.have.been.calledOnce;
    });

  });

  describe('POST /api/systems', function() {

    it('should route to system.controller.create', function() {
      routerStub.post
        .withArgs('/', 'systemCtrl.create')
        .should.have.been.calledOnce;
    });

  });

  describe('PUT /api/systems/:id', function() {

    it('should route to system.controller.update', function() {
      routerStub.put
        .withArgs('/:id', 'systemCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('PATCH /api/systems/:id', function() {

    it('should route to system.controller.update', function() {
      routerStub.patch
        .withArgs('/:id', 'systemCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('DELETE /api/systems/:id', function() {

    it('should route to system.controller.destroy', function() {
      routerStub.delete
        .withArgs('/:id', 'systemCtrl.destroy')
        .should.have.been.calledOnce;
    });

  });

});
