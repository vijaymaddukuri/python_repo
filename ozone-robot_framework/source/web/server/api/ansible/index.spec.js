'use strict';

var proxyquire = require('proxyquire').noPreserveCache();

var ansibleCtrlStub = {
  index: 'ansibleCtrl.index',
  show: 'ansibleCtrl.show',
  create: 'ansibleCtrl.create',
  update: 'ansibleCtrl.update',
  destroy: 'ansibleCtrl.destroy'
};

var routerStub = {
  get: sinon.spy(),
  put: sinon.spy(),
  patch: sinon.spy(),
  post: sinon.spy(),
  delete: sinon.spy()
};

// require the index with our stubbed out modules
var ansibleIndex = proxyquire('./index.js', {
  'express': {
    Router: function() {
      return routerStub;
    }
  },
  './ansible.controller': ansibleCtrlStub
});

describe('Ansible API Router:', function() {

  it('should return an express router instance', function() {
    ansibleIndex.should.equal(routerStub);
  });

  describe('GET /api/ansible', function() {

    it('should route to ansible.controller.index', function() {
      routerStub.get
        .withArgs('/', 'ansibleCtrl.index')
        .should.have.been.calledOnce;
    });

  });

  describe('GET /api/ansible/:id', function() {

    it('should route to ansible.controller.show', function() {
      routerStub.get
        .withArgs('/:id', 'ansibleCtrl.show')
        .should.have.been.calledOnce;
    });

  });

  describe('POST /api/ansible', function() {

    it('should route to ansible.controller.create', function() {
      routerStub.post
        .withArgs('/', 'ansibleCtrl.create')
        .should.have.been.calledOnce;
    });

  });

  describe('PUT /api/ansible/:id', function() {

    it('should route to ansible.controller.update', function() {
      routerStub.put
        .withArgs('/:id', 'ansibleCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('PATCH /api/ansible/:id', function() {

    it('should route to ansible.controller.update', function() {
      routerStub.patch
        .withArgs('/:id', 'ansibleCtrl.update')
        .should.have.been.calledOnce;
    });

  });

  describe('DELETE /api/ansible/:id', function() {

    it('should route to ansible.controller.destroy', function() {
      routerStub.delete
        .withArgs('/:id', 'ansibleCtrl.destroy')
        .should.have.been.calledOnce;
    });

  });

});
