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

(function() {

class AdminController {
  constructor(User) {
    // Use the User $resource to fetch all users
    this.users = User.query();

    this.roles = ['guest', 'user', 'monitor','deploy','configure', 'admin']

  }

  updateRole(user){
    user.$update();
    user.$get();
  }

  delete(user) {
    user.$remove();
    this.users.splice(this.users.indexOf(user), 1);
  }
}

angular.module('ehcOzoneApp.admin')
  .controller('AdminController', AdminController);

})();
