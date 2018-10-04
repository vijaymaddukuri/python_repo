(function(angular, undefined) {
'use strict';

angular.module('ehcOzoneApp.constants', [])

.constant('appConfig', {ozoneVersion:'0.4.8',userRoles:['guest','user','monitor','deploy','configure','admin','superadmin','service'],defaults:{'EHC4.1.1':{}},scriptEngine:{host:'localhost',user:'root',password:'P@ssw0rd@123',inputDirectory:'/opt/ozone-scripts/ehc-python-modules/input',url_check_script:'/opt/ozone-scripts/ehc-python-modules/bin/url_check.sh',configure:'python3.4 /opt/ozone-scripts/ehc-python-modules/bin/configure.py',snapshot:'python3.4 /opt/ozone-scripts/ehc-python-modules/bin/Snapshot.py',monitor:'python3.4 /opt/ozone-scripts/ehc-python-modules/bin/monitor.py',deployVMFromOvfTemplate:'python3.4 /opt/ozone-scripts/ehc-python-modules/bin/Deploy_VM_from_Template.py',projectsFolder:'/data/ehc-builder-projects/',ansibleProjectTemplates:'/opt/ozone-scripts/ehc-ansible-project-templates/'},redis:{host:'localhost',port:6379,scope:'kue'},kue:{host:'localhost',port:'3000'}})

;
})(angular);