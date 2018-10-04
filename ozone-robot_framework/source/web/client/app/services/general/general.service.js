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

angular.module('ehcOzoneApp')
  .service('general', function () {
    // AngularJS will instantiate a singleton by calling "new" on this function

    this.updateDefaultNetworkInfo = function(component,selectedProject){
      if('netmask0' in component && !component.netmask0){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.netmask0 = selectedProject.components.general_info.network_netmask;
        }
      }

      if('network_netmask' in component && !component.network_netmask){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.network_netmask = selectedProject.components.general_info.network_netmask;
        }
      }

      if('network_netmask0_srm' in component && !component.network_netmask0_srm){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.network_netmask0_srm = selectedProject.components.general_info.network_netmask;
        }
      }

      if('gateway' in component && !component.gateway){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.gateway = selectedProject.components.general_info.network_gateway
        }
      }

      if('network_gateway' in component && !component.network_gateway){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.network_gateway = selectedProject.components.general_info.network_gateway
        }
      }

      if('DNS' in component && !component.DNS){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.DNS = selectedProject.components.general_info.domain_name_servers

        }
      }

      if('domain_name_servers' in component && !component.domain_name_servers){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.domain_name_servers = selectedProject.components.general_info.domain_name_servers

        }
      }

      if('network_dns_srm' in component && !component.network_dns_srm){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.network_dns_srm = selectedProject.components.general_info.domain_name_servers

        }
      }

      if('network_dns_srm' in component && !component.network_dns_srm){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.network_dns_srm = selectedProject.components.general_info.network_dns_srm

        }
      }

      if('network_timeservers' in component && !component.network_timeservers){
        if(selectedProject && selectedProject.components && selectedProject.components.general_info){
          component.network_timeservers = selectedProject.components.general_info.network_timeservers

        }
      }

    };

    this.updateDefaultDomainInfo = function(component,selectedProject){
      if(selectedProject && selectedProject.components && selectedProject.components.general_info && selectedProject.components.general_info.domain){

        if('ldapBase' in component){

          var dc = selectedProject.components.general_info.domain.split('.').map(function(item){
            return ('dc=' + item)
          });
          component.ldapBase = dc.join(',');
        }

        if('defaultDomain' in component){
          component.defaultDomain = selectedProject.components.general_info.domain.split('.')[0];
        }

        if('sharedUserName' in component){
          component.sharedUserName = selectedProject.components.general_info.domain.split('.')[0] + '\\administrator';
        }

      }

    }

  });
