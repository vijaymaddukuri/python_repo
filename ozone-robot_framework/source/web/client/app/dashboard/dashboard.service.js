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
  .service('dashboard', function () {
    // AngularJS will instantiate a singleton by calling "new" on this function
    this.getDashboardTiles = function(){
      return [
        {
          title: 'vRealize Automation',
          subtitle: 'vCloud Automation Center',
          objtype:'vmware_vra',
          span:{row : 1, col : 6 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 700
          },
          count : 0,
          type: 'knob',
          caption: '',
          icon: 'computer',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#589ece;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'vSphere vCenter',
          subtitle: '',
          objtype:'vcenter',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#ffc253;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'vRO',
          subtitle: 'vRealize Orchestrator',
          objtype:'vmware_vro',
          span:{row : 1, col : 2 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#589ece;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'vRealize Operations',
          subtitle: '',
          objtype:'vmware_vrops',
          span:{row : 1, col : 2 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#69b169;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'SRM',
          subtitle: 'EMC ViPR SRM',
          objtype:'viprsrm',
          caption: '',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 500
          },
          count : 0,
          type: 'knob',
          icon: 'group_work',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#69b169;border-style:solid;',
          disabledStyle: 'background:white;'
        },

        {
          title: 'vSphere ESXi',
          subtitle: 'Virtual Layer',
          objtype:'vmware_esx',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#ffc253;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'NSX',
          subtitle: 'Network Virtualization',
          objtype:'nsx',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#ffc253;border-style:solid;',
          disabledStyle: 'background:white;'
        },

        {
          title: 'ViPR',
          objtype:'vipr',
          subtitle: 'Storage Automation',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#ffc253;border-style:solid;',
          disabledStyle: 'background:white;'

        },
        {
          title: 'Puppet',
          subtitle: '',
          objtype:'puppet',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: 'red',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#589ece;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'vRealize Business',
          subtitle: 'VMWare',
          objtype:'vmware_vrb',
          span:{row : 1, col : 2 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#69b169;border-style:solid;',
          disabledStyle: 'background:white;'
        },

        {
          title: 'DPA',
          subtitle: 'Data Protection Advisor',
          objtype:'dpa',
          caption: '',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 500
          },
          count : 0,
          type: 'knob',
          icon: 'group_work',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#d25c5c;border-style:solid;',
          disabledStyle: 'background:white;'

        },
        {
          title: 'Avamar',
          subtitle: 'Backup',
          objtype:'avamar',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'false',
          label: '',
          addStyle: 'border:#d25c5c;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'Data Domain',
          subtitle: 'Backup Component',
          objtype:'datadomain',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#d25c5c;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'Log Insight',
          subtitle: 'VMWare vCenter Log Insight',
          objtype:'vmware_loginsight',
          caption: '',
          span:{row : 1, col : 2 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#69b169;border-style:solid;',
          disabledStyle: 'background:white;'
        },
        {
          title: 'EMC Storage Analytics',
          subtitle: '',
          objtype:'storageanalytics',
          span:{row : 1, col : 1 },
          options : {
            width: 100,
            height: 100,
            fgColor: '#8BC34A',
            skin: 'tron',
            thickness: 0.1,
            displayPrevious: true,
            animationDelay: 1000
          },
          count : 0,
          caption: '',
          type: 'knob',
          icon: 'storage',
          isTime: 'true',
          label: 'OK',
          addStyle: 'border:#69b169;border-style:solid;',
          disabledStyle: 'background:white;'
        }
      ];
    }
  });
