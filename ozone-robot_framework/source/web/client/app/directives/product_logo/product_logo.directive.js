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
  .directive('productLogo', function () {
    return {
      templateUrl: 'app/directives/product_logo/product_logo.html',
      restrict: 'EA',
      scope:{
        product: '=',
        size: '=?'
      },
      link: function (scope, element, attrs) {
        var icon_map = {
          "vipr_vip": "vipr",
          "vra":"vmware_vra",
          "vra_primary":"vmware_vra",
          "vra_secondary":"vmware_vra",
          "vra_web_primary":"vmware_vra",
          "vra_web_secondary":"vmware_vra",
          "vra_manager_primary":"vmware_vra",
          "vra_manager_secondary":"vmware_vra",
          "vra_proxy_agent_primary":"vmware_vra",
          "vra_proxy_agent_secondary":"vmware_vra",
          "vra_worker_primary":"vmware_vra",
          "vra_worker_secondary":"vmware_vra",
          "vro":"vmware_vro",
          "vro_primary":"vmware_vro",
          "vro_secondary":"vmware_vro",
          "vrops":"vmware_vrops",
          "log_insight":"vmware_loginsight",
          "vrli":"vmware_loginsight",
          "vra_business":"vmware_vrb",
          "vra_application_services":"vmware_vrapp",
          "nsx":"vmware_nsx",
          "sql":"sql",
          "dep": "ovf",
          "vcn": "vcenter",
          "power-on-ehc":"power-on-ehc",
          "power-off-ehc":"power-off-ehc",
        };

        var _product = scope.product;
        //Fix Test
        if(_product)_product = scope.product.toLowerCase();
        if(icon_map[_product])scope.img_src = "/assets/images/product_icons/" + icon_map[_product] + "_logo_small.png";
        else if(_product)scope.img_src = "/assets/images/product_icons/" + _product + "_logo_small.png";
        else scope.img_src = "/assets/images/product_icons/workflow.png";

        if(!scope.size){
          scope.size = 'medium'
        }

        if(scope.size=== 'medium'){
          scope.width = '50px';
        }else if(scope.size=== 'small'){
          scope.width = '25px';
        }else if(scope.size=== 'large'){
          scope.width = '100px';
        }



      }
    };
  });
