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
(function(){

class SnapshotComponent {
  constructor($scope,$mdDialog,$timeout,projects,snapshot,messageus,ansi2html,$sce, tile, Auth,$rootScope) {
    $scope.dataLoaded = false;

    $scope.view = 'table';
    $scope.selectedComponents = [];

    //$scope.Candidates = ['vmware_vro','vipr','vmware_vra','vmware_vrb','vmware_vrops','vmware_loginsight'];
    $scope.Candidates = ["vipr_vip","vra_primary","vra_secondary","vra_web_primary","vra_web_secondary","vra_manager_primary","vra_manager_secondary","vra_proxy_agent_primary","vra_proxy_agent_secondary","vra_worker_primary","vra_worker_secondary","vro_primary","vro_secondary","vrops","log_insight","vra_business","vra_application_services","nsx","cloud_sql_server"];

    $scope.hasDeployRole = Auth.hasRole('deploy');

    $scope.getLogsService = snapshot.getLogs;

    $scope.vmids = {};

    $scope.showEmailUs = function(ev){
      messageus.showInputDialog(ev,"Count me In!","Tell us about yourself.","green");
    };


    $scope.selectedProjectChanged = function(){
      if(!$scope.hasDeployRole)return;
      $scope.tiles = [];
      $scope.vcenter = {};
      if(!(projects.selectedProject && projects.selectedProject.components))return;
      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.vcenter){
        $scope.vcenter = projects.selectedProject.components.vcenter
      }

      if(projects.selectedProject && projects.selectedProject.components && projects.selectedProject.components.vmids)
        $scope.vmids = projects.selectedProject.components.vmids;

      tile.getComponentTiles(projects.selectedProject,$scope.Candidates,$scope.tiles,$scope.getSnapshotInfo);
      $scope.listAllSnapshots();
    };

    /*var baseTile = tile.getBaseTile();*/

    $scope.tiles = [];
    $scope.refreshLog = {value: false};
    $scope.result = null;
    $scope.progressType='blue';

    /**
     * Get Snapshot Info
     * @param component
     */
    $scope.getSnapshotInfo = function(component){

      component.loading = true;
      component.state = 'LOADING';
      component.statusText = 'Loading';
      snapshot.get(projects.selectedProject._id, component.objectType, function(successResponse) {
          component.loading = false;
          component.configureObject = successResponse.data[successResponse.data.length - 1];
          component.jobObjects = successResponse.data;

        if(component.configureObject && component.configureObject.logfile){
            var matches = component.configureObject.logfile.match(/.*_(.*).log/);
            if(matches.length > 1)component.logtime = matches[1];
          }

          component.buttonText = 'Snap';
          component.buttonIcon = 'add_a_photo';


          if(component.configureObject){
            component.state = 'LOADING';
            component.statusText = 'Loading';
            $scope.refreshLogs(component);
            //$scope.listSnapshots(component)

          }else{
            component.state = '';
          }
        },
        function(errorResponse){
          component.loading = false;
          component.statusText = 'Configure';
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
        });
    };

    /**
     * Show Snapshots
     * @param component
     * @param responseData
     */
    $scope.showSnapshots = function(component, responseData){
      //component.logOutput = $sce.trustAsHtml(ansi2html.toHtml(responseData).replace(/\n/g, "<br>"));

      var trackingItems = $scope.getTrackingItems(responseData);
      angular.forEach(trackingItems,function(item){
        if(item.type && item.type == "ERROR"){
          item.icon = 'error';
          item.color = 'red';
          component.trackingItems.push(item)
        }
        if(item.type && item.type == "INFO"){
          item.icon = 'info';
          item.color = 'grey';
          component.trackingItems.push(item)
        }
        component.stepsAvailable = true
      });


      var resultItems = $scope.getResultItems(responseData);
      component.trackingItems = [];
      component.snapshotItems = [];
      angular.forEach(resultItems,function(item){
        if('snapshot' in item){
          item.icon = 'photo_camera';
          item.color = 'grey';
          item.message = item.snapshot.name;
          item.createTime = new Date(item.snapshot.createTime);
          item.snapshotId = item.snapshot.snapshotID;
          component.snapshotItems.push(item)
        }
        //component.showSnaps = {value:false};
        component.snapsAvailable = true
      });

    };


    /**
     * Show Snapshots
     * @param component
     * @param responseData
     */
    $scope.showAllSnapshots = function(responseData){
      //component.logOutput = $sce.trustAsHtml(ansi2html.toHtml(responseData).replace(/\n/g, "<br>"));

      var trackingItems = $scope.getTrackingItems(responseData);
      angular.forEach(trackingItems,function(item){
        if(item.type && item.type == "ERROR"){
          item.icon = 'error';
          item.color = 'red';
        }
        if(item.type && item.type == "INFO"){
          item.icon = 'info';
          item.color = 'grey';
        }
      });

      var resultItems = $scope.getResultItems(responseData);

      angular.forEach($scope.tiles, component => {
        component.trackingItems = [];
        component.snapshotItems = [];
        component.expandIcon = 'keyboard_arrow_right';
        if(!component.showSnaps)component.showSnaps = {value:false};

        angular.forEach(resultItems,function(item){
          if('snapshot' in item && item.snapshot.VMID && item.snapshot.VMID==$scope.vmids[component.objectType]){
            item.icon = 'photo_camera';
            item.color = 'grey';
            item.message = item.snapshot.name;
            item.createTime = new Date(item.snapshot.createTime);
            item.snapshotId = item.snapshot.snapshotID;
            item.vmId = item.snapshot.VMID;
            component.snapshotItems.push(item);

          }
          //component.showSnaps = true;
          component.snapsAvailable = true
        });
      })
    };


    $scope.expandRow = function(component){
      component.expandIcon = component.expandIcon == 'keyboard_arrow_down' ? 'keyboard_arrow_right' : 'keyboard_arrow_down';
      component.showSnaps.value = !component.showSnaps.value
    }

    /**
     * Get Logs
     * @param component
     */
    $scope.getLogs = function(component){
      component.loading = true;

      snapshot.getLogs(component.configureObject,function(successResponse){
          component.loading = false;
          //var ansi2html_logs = ansi2html.toHtml(successResponse.data)
          //component.escapedLogs = mdescape.markdown_escape(ansi2html_logs ).replace(/\n/g, "<br>");

          if(typeof successResponse.data == 'object')successResponse.data = successResponse.data.join("\n");

          component.logOutput = $sce.trustAsHtml(ansi2html.toHtml(successResponse.data).replace(/\n/g, "<br>"));
          component.logContent = successResponse.data;
          //component.logOutput = successResponse.data.replace(/\n/g, "<br>")

          var trackingItems = $scope.getTrackingItems(successResponse.data);


          var re = /Stream :: close :: code: [1-9][0-9]*,/;
          var m = re.exec(successResponse.data);

          if(m !== null){
            component.progress = -1;
          }else{
            component.progress = $scope.getProgress(trackingItems);
          }

          // if(successResponse.data.indexOf("Stream :: close :: code: 1, signal: undefined")>-1){
          //   component.progress = -1;
          // }else{
          //   component.progress = $scope.getProgress(trackingItems);
          // }

          // progress : 100 = Completed successfully
          // progress : -200 = Warning
          // progress : -1 error
          // If progress is not warning and not completed and process finished, error
          if(component.progress != -200 && component.progress < 100 && successResponse.data.indexOf("Stream :: close :: code: 0, signal: undefined")>-1){
            component.progress = -1;
          }

          var customMessages = {
            'inProgress' : 'Creating',
            'done' : 'Created'
          };

          if(component.configureObject.operation == 'revert'){
            customMessages = {
              'inProgress' : 'Reverting',
              'done' : 'Reverted'
            }
          }else if(component.configureObject.operation == 'delete'){
            customMessages = {
              'inProgress' : 'Deleting',
              'done' : 'Deleted'
            }
          }

          component.messageTexts = customMessages;


          //$scope.showTrackingItems(component,trackingItems);
          if(component.progress == 100){
            component.progressType='green';
            component.label = '100%';
            component.refreshLog = false;
            component.statusIcon = 'done_all';
            component.errmsg = 'Click to Create Snapshot';
            component.buttontheme = 'green';
            component.statusText = customMessages.done;
            component.state = 'SUCCESS';
            component.logsAvailable = true;
            component.stepsAvailable = true;
            $scope.listAllSnapshots();
          }else if(component.progress == -200){
            component.progress = 100;
            component.progressType='orange';
            component.label = '!';
            component.options.fgColor = 'orange';
            component.statusIcon = 'done_all';
            component.state = 'WARNING';
            component.errmsg = 'Click to Retry';
            component.buttontheme = 'orange';
            component.refreshLog = false;
            component.statusText = customMessages.done;
            component.logsAvailable = true;
            component.stepsAvailable = true;
            //component.showLog = true;
          }else if(component.progress < 0){
            component.progress = component.progress*-1;
            component.progressType='red';
            component.label = '!';
            component.options.fgColor = 'red';
            component.statusIcon = 'error';
            component.errmsg = 'Click to Retry';
            component.statusText = 'Snap';
            component.state = 'FAIL';
            component.buttontheme = 'red';
            component.refreshLog = false;
            component.statusText = 'Failed';
            component.logsAvailable = true;
            component.stepsAvailable = true;
            //component.showLog = true;
          }
          else{
            component.logsAvailable = true;
            component.stepsAvailable = true;
            component.buttontheme = 'default';
            component.statusIcon = 'refresh';
            component.state = 'RUNNING';
            component.progressType='blue';
            component.label = component.progress + '%';
            component.statusText = customMessages.inProgress;
            component.options.fgColor = '#8BC34A';
            //component.showSteps = true;
            if(!component.refreshLog){
              component.refreshLog = true;
              $scope.getLogs(component);
            }

          }

        },
        function(errorResponse){
          component.loading = false;

          console.log("errorResponse ="+ JSON.stringify(errorResponse.data))
        })
    };

    /**
     * Get Progress
     * @param trackingItems
     * @returns {number}
     */
    $scope.getProgress = function(trackingItems){
      var i = 0;
      var progress = 0;
      var error = false;
      var all_success_with_warnings = false;


      angular.forEach(trackingItems,function(item){
        if(!item)return
        if(item.type==='PROGRESS'){
          if(item.message == 'completed'){
            progress = 100
          }else{
            if(progress < parseInt(item.message) )
              progress = parseInt(item.message)
          }

        }
        if(item.type==='ERROR') {
          error = true
        }
        if(item.type==='ALLSUCCESSWARNING') {
          all_success_with_warnings = true
        }
      });

      if(all_success_with_warnings) return -200;
      if(error) return -1 * (progress || 1);
      return progress;

    };

    /**
     * Show Tracking Items on screen
     * @param component
     * @param trackingItems
     */
    $scope.showTrackingItems = function(component,trackingItems){
      var i = 0;
      var unique_dict = {};
      component.trackingItems = [];
      angular.forEach(trackingItems,function(item){
        if(item.type!='PROGRESS'){
          //unique_dict[item.message] = item.type;
          //component.trackingItems.push(item)
          if(item.type === 'ALLSUCCESS') {
            item.icon = 'done_all';
            item.color = '#2e7d32'
          }else if(item.type === 'ALLSUCCESSWARNING') {
            item.icon = 'done_all';
            item.color = 'orange'
          }else if(item.type === 'SUCCESS'){
            item.icon = 'check_circle';
            item.color = '#2e7d32'
          }else if(item.type === 'ERROR'){
            item.icon = 'error';
            item.color = '#c62828'
          }else if(item.type === 'RUNNING'){
            item.icon = 'refresh';
            item.color = '#1565c0'
          }else if(item.type === 'PENDING'){
            item.icon = 'alarm';
            item.color = '#1565c0'
          }else{
            item.icon = 'error';
            item.color = 'orange'
          }

          var trackItemExists = false;
          angular.forEach(component.trackingItems,function(trackItem){
            if(trackItem.message == item.message){
              trackItemExists = true;
              trackItem.type = item.type;
              trackItem.icon = item.icon;
              trackItem.color = item.color;
            }
          });

          if(!trackItemExists){
            component.trackingItems.push(item)
          }

        }
      });

      //component.trackingItems = unique_dict

    };

    /**
     * Get Tracking Items
     * @param logs
     * @returns {*}
     */
    $scope.getTrackingItems = function(logs){
      if(logs.indexOf('ozone_display_item') < 0){
        return null
      }

      var filtered_results = [];
      var re = /({.*})/gm;
      var m;

      while ((m = re.exec(logs)) !== null) {
        if (m.index === re.lastIndex) {
          re.lastIndex++;
        }
        // View your result using the m-variable.
        // eg m[0] etc.

        try{
          var trackingItem = JSON.parse(m[1])['ozone_display_item'];
          if(trackingItem)filtered_results.push(trackingItem);
        }
        catch(e){
          console.log("Error - " + e);
          return {'type':'WARNING','message':'Error parsing step from log'}
        }

      }

      return filtered_results;

    };

    /**
     * Get Result Items
     * @param logs
     * @returns {*}
     */
    $scope.getResultItems = function(logs){

      if(logs.indexOf('ozone_result_item') < 0){
        return null
      }

      var filtered_results = logs.split("\n").filter(function(item){return item.indexOf('ozone_result_item') > -1});
      return filtered_results.map(function(item){
        try{
          return JSON.parse(item)['ozone_result_item'];
        }
        catch(e){
          console.log("Error - " + e);
          return {'type':'WARNING','message':'Error parsing step from log'}
        }
      });

    };

    /**
     * Refresh Logs
     * @param component
     */
    $scope.refreshLogs = function(component){
      if(component.logRefreshTimer){
        $timeout.cancel( component.logRefreshTimer );
      }

      $scope.getLogs(component);

      component.logRefreshTimer = $timeout(
        function(){
          if(component.refreshLog) {
            $scope.refreshLogs(component);
          }
        },
        6000
      );

      $scope.$on(
        "$destroy",
        function( event ) {
          $timeout.cancel( component.logRefreshTimer );
        }
      );

    };

    /**
     * Show Confirm Button
     * @param ev
     * @param component
     */
    $scope.showConfirm = function(ev,component,type, snapshotId) {
      // Appending dialog to document.body to cover sidenav in docs app
      var confirm = $mdDialog.confirm()
        .title(type + ' snapshot')
        .textContent('Are you sure you want to ' + type + ' snapshot?')
        .ariaLabel(type + ' snapshot')
        .targetEvent(ev)
        .ok('Yes')
        .cancel('No');
      $mdDialog.show(confirm).then(function() {
        if(type == 'revert')$scope.revertSnapshot(component,snapshotId);
        else if(type == 'delete')$scope.deleteSnapshot(component,snapshotId);
      }, function() {

      });
    };

    /**
     * Show Confirm All Snap
     * @param ev
     */
    $scope.confirmAllSnap = function(ev) {
      // Appending dialog to document.body to cover sidenav in docs app
      var confirm = $mdDialog.confirm()
        .title('Create Snapshot')
        .textContent('Are you sure you want to create a new snapshot of all items at once?')
        .ariaLabel('Create Snapshot')
        .targetEvent(ev)
        .ok('Yes')
        .cancel('No');
      $mdDialog.show(confirm).then(function() {
        $scope.promptSnapshotName(ev,null,true);
      }, function() {

      });
    };

    /**
     * Show Alert
     * @param ev
     */
    $scope.showAlert = function(ev) {
      // Appending dialog to document.body to cover sidenav in docs app
      // Modal dialogs should fully cover application
      // to prevent interaction outside of dialog
      $mdDialog.show(
        $mdDialog.alert()
          .parent(angular.element(document.querySelector('#popupContainer')))
          .clickOutsideToClose(true)
          .title('Snapshot name is required')
          .textContent('A snapshot name is required for creating a snapshot.')
          .ok('Got it!')
          .targetEvent(ev)
      );
    };


    /**
     * Prompt Snapshot Name
     * @param ev
     * @param component
     * @param all
     */
    $scope.promptSnapshotName = function(ev,component,all) {
      // Appending dialog to document.body to cover sidenav in docs app
      // var confirm = $mdDialog.prompt()
      //   .title('Enter snapshot name')
      //   .textContent('Enter a name to be associated with the snapshot')
      //   .placeholder('Snapshot name')
      //   .targetEvent(ev)
      //   .ok('Ok')
      //   .cancel('Cancel');
      // $mdDialog.show(confirm).then(function(result) {
      //   if(!result){
      //     $scope.showAlert()
      //   }else{
      //     if(all){
      //       $scope.createAllSnapshot(result);
      //     }else{
      //       $scope.createSnapshot(component,result);
      //     }
      //
      //   }
      // }, function() {
      //
      // });

      $mdDialog.show({
        controller: 'SnapshotNameDialogueCtrl',
        templateUrl: '/app/snapshot/snapshot_name_dialogue/snapshot_name_dialogue.html',
        parent: angular.element(document.body),
        targetEvent: ev,
        clickOutsideToClose: true,
      }).then(function(snapshotData) {
        if(!(snapshotData && snapshotData.snapshotName)){
          $scope.showAlert()
        }else{
          if(all){
            $scope.createAllSnapshot(snapshotData.snapshotName, snapshotData.shutdownGuest, snapshotData.snapshotDescription);
          }else{
            $scope.createSnapshot(component, snapshotData.snapshotName, snapshotData.shutdownGuest, snapshotData.snapshotDescription);
          }

        }
      }, function() {

      });

    };


    /**
     * Prompt Snapshot Name to Revert
     * @param ev
     */
    $scope.promptSnapshotNameToRevertAll = function(ev) {

      var snapshot_list = [];

      angular.forEach($scope.selectedComponents, function(component){

        angular.forEach(component.snapshotItems, snapshotItem => {

          snapshot_list.push({
            component_name: component.title,
            object_type: component.objectType,
            name: snapshotItem.message,
            create_time: snapshotItem.createTime,
            vmid: snapshotItem.vmId,
            snapshotId: snapshotItem.snapshotId,
            component: component
          });

        });
      });



      $mdDialog.show({
        controller: 'RevertAllCtrl',
        templateUrl: '/app/snapshot/revert_all/revert_all.html',
        parent: angular.element(document.body),
        targetEvent: ev,
        clickOutsideToClose: true,
        locals: {
          snapshots: snapshot_list
        },
      }).then(function(selectedSnapshots) {

          angular.forEach(selectedSnapshots, selectedSnapshot =>{
            $scope.executeSnapshotJob(selectedSnapshot.component, selectedSnapshot.snapshotId, 'revert');
          })

        }, function() {

        });
    };

    var stringConstructor = "test".constructor;
    var arrayConstructor = [].constructor;
    var objectConstructor = {}.constructor;

    /**
     * List Snapshots
     * @param component
     */
    $scope.listSnapshots = function(component){

      component.trackingItems = [];

      var snapshotData = {
        type: component.objectType,
        operation: 'list',
        vmid: $scope.vmids[component.objectType],
        snapshot: '',
        snapshotdescription: '',
        refid: projects.selectedProject._id + "_" + component.objectType,
        project: projects.selectedProject
      };
      component.liststatusIcon = 'refresh';
      snapshot.listSnapshots(snapshotData,
        function(successResponse){
          component.liststatusIcon = '';

          if(successResponse.data.constructor == objectConstructor){
            successResponse.data = JSON.stringify(successResponse.data)
          }
          $scope.showSnapshots(component, successResponse.data)
        },
        function(errorResponse){
          component.liststatusIcon = 'error';
          component.errmsg = errorResponse.data;
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data));
          if(component.logRefreshTimer){
            $timeout.cancel( component.logRefreshTimer );
          }
          component.logOutput = errorResponse.data;
        });
    };

    /**
     * List All Snapshots
     * @param component
     */
    $scope.listAllSnapshots = function(){

      var vmids = []
      angular.forEach($scope.vmids,(vmid,key) => {vmids.push(vmid)})



      var snapshotData = {
        type: 'all',
        operation: 'list',
        vmid: vmids.join(','),
        snapshot: '',
        snapshotdescription: '',
        refid: projects.selectedProject._id + "_All" ,
        project: projects.selectedProject
      };
      //component.liststatusIcon = 'refresh';
      snapshot.listSnapshots(snapshotData,
        function(successResponse){
          //component.liststatusIcon = '';

          if(successResponse.data.constructor == objectConstructor){
            successResponse.data = JSON.stringify(successResponse.data)
          }
          $scope.showAllSnapshots(successResponse.data);
          //$scope.showSnapshots(component, successResponse.data)
        },
        function(errorResponse){
          //component.liststatusIcon = 'error';
          //component.errmsg = errorResponse.data;
          console.log("errorResponse ="+ JSON.stringify(errorResponse.data));
          // if(component.logRefreshTimer){
          //   $timeout.cancel( component.logRefreshTimer );
          // }
          // component.logOutput = errorResponse.data;
        });
    };

    /**
     * Create Snapshot
     * @param component
     * @param snapshotName
     */
    $scope.createSnapshot = function(component, snapshotName, shutdownGuest, snapshotDescription){
      $scope.executeSnapshotJob(component, snapshotName, 'create', shutdownGuest, snapshotDescription);
    };

    /**
     * Revert Snapshot
     * @param component
     * @param snapshotId
     */
    $scope.revertSnapshot = function(component, snapshotId){
      $scope.executeSnapshotJob(component, snapshotId, 'revert');
    };

    /**
     * Delete Snapshot
     * @param component
     * @param snapshotId
     */
    $scope.deleteSnapshot = function(component, snapshotId){
      $scope.executeSnapshotJob(component, snapshotId, 'delete');
    };

    /**
     * Execute Snapshot Create or Revert Job
     * @param component
     * @param snapshotName - SnapshotName for Creation and SnapshotId for Deletion/Revert
     * @param operation
     * @param shutdownGuest
     * @param snapshotDescription
     * @returns {*}
     */
    $scope.executeSnapshotJob = function(component, snapshotName, operation, shutdownGuest, snapshotDescription){

      if(!($scope.vmids[component.objectType])){
        return console.log("Skipping snapshot creation of " + component.objectType + " as no VM ID found.")
      }

      component.trackingItems = [];

      var snapshotData = {
        type: component.objectType,
        operation: operation,
        vmid: $scope.vmids[component.objectType],
        snapshotname: snapshotName,
        shutdownGuest: shutdownGuest,
        snapshotId: snapshotName, //Used for Revert
        snapshotdescription: snapshotDescription,
        refid: projects.selectedProject._id + "_" + component.objectType,
        project: projects.selectedProject
      };

      component.statusIcon = 'refresh';
      component.statusText = 'Creating';
      if(operation == 'revert')component.statusText = 'Reverting';
      else if(operation == 'delete')component.statusText = 'Deleting';
      component.progress = 0;
      //component.showSnaps = {value:false};

      snapshot.create(snapshotData,
        function(successResponse){


          component.refreshLog = true;
          component.configureObject = successResponse.data;
          component.buttontheme = 'green';

          if(component.configureObject && component.configureObject.logfile){
            var matches = component.configureObject.logfile.match(/.*_(.*).log/);
            if(matches.length > 1)component.logtime = matches[1];
          }

          $scope.refreshLogs(component);

        },
        function(errorResponse){
          console.log("SNAPSHOT Error Response")
          component.refreshLog = false;
          component.statusIcon = 'error';
          component.buttontheme = 'red';
          component.errmsg = errorResponse.data;

          if(component.logRefreshTimer){
            $timeout.cancel( component.logRefreshTimer );
          }
          component.logOutput = errorResponse.data;
        });

    };


    $scope.createAllSnapshot = function(snapshotName, shutdownGuest, snapshotDescription){
      angular.forEach($scope.selectedComponents,function(tile,index){
        $scope.createSnapshot(tile,snapshotName, shutdownGuest, snapshotDescription)
      })
    };

    projects.subscribeCustom($scope,$scope.selectedProjectChanged);

    if(!$scope.dataLoaded){
      $scope.selectedProjectChanged()
    }

    //projects.refresh();
    //$rootScope.$emit('notify-refresh-projects');

  }
}

angular.module('ehcOzoneApp')
  .component('snapshot', {
    templateUrl: 'app/snapshot/snapshot.html',
    controller: SnapshotComponent
  });

})();
