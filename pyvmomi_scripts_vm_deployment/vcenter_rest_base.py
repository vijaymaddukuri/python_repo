import os
import tarfile
import urllib2
import httplib
import ssl
import time
import atexit
import re
import requests
from pyVmomi import vim
from pyVim import connect
from pyVim.connect import Disconnect
from robot.api import logger
from time import sleep
from threading import Thread

class VCenterLib(object):

    def __init__(self, credentials):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.hostname = credentials[0]
        self._port = '443'
        self.vCenter_cre_dict = {'host': credentials[0],
                                 'username': credentials[1],
                                 'password': credentials[2],
                                 'port': self._port
                                 }
        self._init_connection_with_vCenter()

    def _init_connection_with_vCenter(self):
        """
        Establish connection with vCenter as a vSphere administrator
        :return: True or raise error
        """
        if not self.vCenter_cre_dict:
            raise RuntimeError("Please input vCenter credentials in init_connections first!")
        if (not self.vCenter_cre_dict["host"]) or (not str(self.vCenter_cre_dict["host"]).strip()):
            raise ValueError("vCenter name - invalid value or type")
        if (not self.vCenter_cre_dict["username"]) or (not str(self.vCenter_cre_dict["username"]).strip()):
            raise ValueError("vCenter username - invalid value or type")
        if (not self.vCenter_cre_dict["password"]) or (not str(self.vCenter_cre_dict["password"]).strip()):
            raise ValueError("vCenter password - invalid value or type")
        if (not self.vCenter_cre_dict["port"]) or (not str(self.vCenter_cre_dict["port"]).strip()):
            self.vCenter_cre_dict["port"] = 443
        elif str(self.vCenter_cre_dict["port"]).strip().isdigit():
            self.vCenter_cre_dict["port"] = int(str(self.vCenter_cre_dict["port"]).strip())
        else:
            raise ValueError("vCenter port - invalid value or type")
        try:
            self.vCenter_cre_dict["si"] = connect.Connect(self.vCenter_cre_dict["host"],
                                                          self.vCenter_cre_dict["port"],
                                                          self.vCenter_cre_dict["username"],
                                                          self.vCenter_cre_dict["password"])
        except vim.fault.HostConnectFault as e:
            raise RuntimeError(e.msg)
        except IOError:
            raise RuntimeError("Cannot connect to specified host using specified vCenter username and password")
        atexit.register(Disconnect, self.vCenter_cre_dict["si"])
        self.vCenter_cre_dict["content"] = self.vCenter_cre_dict["si"].RetrieveContent()
        return True

    def _get_obj(self, vim_type, vm_name):
        """
        Return a vSphere object associated with a given text name an vim type
        :param: content The content object of current session
        :param: vim_type Specific type of the object such as vim.VirtualMachine
        :param: vm_name The given text name if the vm
        :return: The target vSphere object
        """
        obj = None
        self._init_connection_with_vCenter()
        content = self.vCenter_cre_dict["content"]
        container = content.viewManager.CreateContainerView(content.rootFolder, vim_type, True)
        for c in container.view:
            if c.name == vm_name:
                obj = c
                break
        # self._close_connection_with_vCenter()
        return obj

    def get_vm_folder(self, vm_name):
        if (not vm_name) or (not str(vm_name).strip()):
            raise ValueError("virtual machine name - invalid value or type")
        vm_obj = self._get_obj([vim.VirtualMachine], vm_name)
        if vm_obj:
            logger.info('{} located in {} folder'.format(vm_name,vm_obj.parent.name), True, True)
            return vm_obj.parent.name
        else:
            return None

    def _close_connection_with_vCenter(self):
        """
        Close current connection with vCenter
        """
        if self.vCenter_cre_dict["si"]:
            connect.Disconnect(self.vCenter_cre_dict["si"])
            self.vCenter_cre_dict["si"] = None
            self.vCenter_cre_dict["content"] = None

    def _get_vm_info( self,vc_cred,vm_name,vim_type=[vim.VirtualMachine]):
        """
        Return a vSphere object associated with a given text name an vim type
        :param: content The content object of current session
        :param: vim_type Specific type of the object such as vim.VirtualMachine
        :param: vm_name The given text name if the vm
        :return: The target vSphere object uuid
        """
        vm_info={}
        obj = VCenterLib(vc_cred)
        obj._init_connection_with_vCenter()
        content = obj.vCenter_cre_dict["content"]
        container = content.viewManager.CreateContainerView(content.rootFolder, vim_type, True)
        for cont in container.view:
            if cont.name == vm_name:
                vm_info = {'uuid': cont.config.uuid, 'os_type': cont.guest.guestFamily, 'vm_state': cont.guest.guestState,
                           'network_name': cont.network[0].name, 'parent_folder': cont.parent.name}
                break
        # self._close_connection_with_vCenter()
        return vm_info

    def _get_vm_host_name_and_ip( self,vc_cred,vm_name,vim_type=[vim.VirtualMachine]):
        """
        Return a vSphere object hostname and ip associated with a given text name an vim type
        :param: content The content object of current session
        :param: vim_type Specific type of the object such as vim.VirtualMachine
        :param: vm_name The given text name if the vm
        :return: The target vSphere object hostname and ip address
        """
        vm_info={}
        hostname, ipaddress = None, None
        obj = VCenterLib(vc_cred)
        obj._init_connection_with_vCenter()
        content = obj.vCenter_cre_dict["content"]
        container = content.viewManager.CreateContainerView(content.rootFolder, vim_type, True)
        for cont in container.view:
            if cont.name == vm_name:
                ipaddress = cont.summary.guest.ipAddress
                hostname = cont.summary.guest.hostName
                # Removing the domain name if exists in hostname
                hostname = hostname.split('.')[0]
                break
        return hostname, ipaddress


    def _upload_file_in_vm(self,vc_cred,vm_details,deployed_vm):
        """
        Uploads a file in the virtual machine
        :param: vc_cred the vcenter credentials
        :param: vm_details virtual machine login credential
        :param: delpoyed_vm The given text name if the vm
        """
        try:
            service_instance = connect.SmartConnect(host=vc_cred[0],
                                                    user=vc_cred[1],
                                                    pwd=vc_cred[2],
                                                    port='443')
            atexit.register(connect.Disconnect, service_instance)
            content = service_instance.RetrieveContent()
            vm_info = self._get_vm_info(vc_cred,deployed_vm)
            assert (vm_info['vm_state'].lower() == 'running'),"Can't upload file if vm is not running"
            sleep(30)
            creds = vim.vm.guest.NamePasswordAuthentication(username=vm_details[0], password=vm_details[1])
            with open(__file__, 'rb') as myfile:
                args = myfile.read()
            vm = content.searchIndex.FindByUuid(None,vm_info['uuid'],True)
            file_attribute = vim.vm.guest.FileManager.FileAttributes()
            path_for_linux = '/root/test1.txt' if str(vm_details[0]) == 'root' else '/home/'+ str(vm_details[0]) + "/test1.txt"
            logger.debug("Deployed vm belongs to {} family".format(vm_info['os_type']))
            if str(vm_info['os_type']).find('windows') != -1:
                url = content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(vm, creds,
                                                      "c:\\test1.txt",file_attribute,len(args), True)
            else:
                url = content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(vm, creds,
                                                      path_for_linux,file_attribute,len(args), True)

            url = re.sub(r"^https://\*:", "https://" + str(vc_cred[0]) + ":", url)
            resp = requests.put(url, data=args, verify=False)
            if not resp.status_code == 200:
                raise RuntimeError("Error while uploading file in the virtual machine")
            else:
                logger.info("Successfully uploaded file in the virtual machine", False, True)
        except Exception as msg:
            logger.error(msg)

    def _delete_file_in_vm(self,vc_cred,vm_details,deployed_vm):
        """
        Uploads a file in the virtual machine
        :param: vc_cred the vcenter credentials
        :param: vm_details virtual machine login credential
        :param: delpoyed_vm The given text name if the vm
        """
        try:
            _port = '443'
            service_instance = connect.SmartConnect(host=vc_cred[0],
                                                    user=vc_cred[1],
                                                    pwd=vc_cred[2],
                                                    port=_port)
            atexit.register(connect.Disconnect, service_instance)
            content = service_instance.RetrieveContent()
            vm_info = self._get_vm_info(vc_cred,deployed_vm)
            assert (vm_info['vm_state'].lower() == 'running'),"Can't delete file if vm is not running"
            creds = vim.vm.guest.NamePasswordAuthentication(username=vm_details[0], password=vm_details[1])
            vm = content.searchIndex.FindByUuid(None,vm_info['uuid'],True)
            logger.info("Going to delete file test1.txt from virtual machine")
            path_for_linux = '/root/test1.txt' if str(vm_details[0]) == 'root' else '/home/' + str(vm_details[0]) + "/test1.txt"
            try:
                content.guestOperationsManager.fileManager.DeleteFileInGuest(vm ,creds,path_for_linux)
                logger.info("Successfully deleted file in virtual machine", False, True)
            except:
                logger.error("Failed to delete file in virtual machine")
        except Exception as msg:
            logger.error(msg)

    def _check_file_exist_in_vm(self,vc_cred,vm_details,deployed_vm):
        """
        Uploads a file in the virtual machine
        :param: vc_cred the vcenter credentials
        :param: vm_details virtual machine login credential
        :param: delpoyed_vm The given text name if the vm
        """
        try:
            _port = '443'
            service_instance = connect.SmartConnect(host=vc_cred[0],
                                                    user=vc_cred[1],
                                                    pwd=vc_cred[2],
                                                    port=_port)
            atexit.register(connect.Disconnect, service_instance)
            content = service_instance.RetrieveContent()
            vm_info = self._get_vm_info(vc_cred,deployed_vm)
            assert (vm_info['vm_state'].lower() == 'running'),"Can't check file if vm is not running"
            creds = vim.vm.guest.NamePasswordAuthentication(username=vm_details[0], password=vm_details[1])
            vm = content.searchIndex.FindByUuid(None,vm_info['uuid'],True)
            flag = False
            logger.debug("Deployed vm belongs to {} family".format(vm_info['os_type']))
            dir_for_linux = '/root' if str(vm_details[0]) == 'root' else '/home/' + str(vm_details[0])
            if re.search(vm_info['os_type'],'windows',re.I):
                file_in_path=content.guestOperationsManager.fileManager.ListFilesInGuest(vm, creds, "c:\\")
                for file in range(0,len(file_in_path.files)):
                    if file_in_path.files[file].path == 'test1.txt':
                        logger.info("File test1.txt found in the virtual machine",True)
                        flag = True
                        break

            else:
                file_in_path = content.guestOperationsManager.fileManager.ListFilesInGuest(vm,creds,dir_for_linux)
                for file in range(0,len(file_in_path.files)):
                    if file_in_path.files[file].path == 'test1.txt':
                        logger.info("File test1.txt found in the virtual machine", True)
                        flag = True
                        break
            assert flag , "File test1.txt doesn't exist"
            except Exception as msg:
            logger.error(msg)

    def revert_vm_to_a_snapshot(self, vm_name, snapshot_name):
        vm_obj = self._get_obj([vim.VirtualMachine], vm_name)
        snapshot_trees = vm_obj.snapshot.rootSnapshotList
        vm_snapshot = None
        vm_snapshot = self.find_snapshot_by_name(snapshot_trees, snapshot_name)
        if not vm_snapshot:
            logger.error("Didn't find snapshot {0} in VM {1}.".format(snapshot_name,vm_name), True)
            raise AssertionError("Didn't find snapshot {0} in VM {1}.".format(snapshot_name,vm_name))
        task = vm_snapshot.RevertToSnapshot_Task()
        while task.info.state == vim.TaskInfo.State.running:
            time.sleep(30)
        return True

    def find_snapshot_by_name(self,snapshot_trees,snapshot_name):
        snapshot = None
        if snapshot_trees:
            for tree in snapshot_trees:
                if tree.name == snapshot_name:
                    logger.info("find snapshot",True,True)
                    snapshot = tree.snapshot
                    break
                elif tree.childSnapshotList:
                    snapshot=self.find_snapshot_by_name(tree.childSnapshotList, snapshot_name)
                    if snapshot:
                        break
        return snapshot

    def power_on_vm(self, vm_name):
        vm_obj = self._get_obj([vim.VirtualMachine], vm_name)
        self._init_connection_with_vCenter()
        task = None
        if vm_obj.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
            task = vm_obj.poweron()
            while task.info.state == vim.TaskInfo.State.running:
                time.sleep(30)
            if task.info.state != vim.TaskInfo.State.success:
                raise task.info.error
            self._close_connection_with_vCenter()
            return "Power on VM {0} successfully".format(vm_name)
        self._close_connection_with_vCenter()
        return "VM {0} is already powered on.".format(vm_name)

    def get_cluster(self, cluster):
        """get cluster from pyvmomi content
        """
        clusterobj = self._get_obj([vim.ClusterComputeResource],
                                  cluster)
        return clusterobj

    @staticmethod
    def get_uid(element):
        assert element, 'get_uid needs a non empty input'
        return str(element).split(":")[-1].rstrip("'")

    def keep_lease_alive(self, lease):
        """
        Keeps the lease alive while POSTing the VMDK.
        """
        while (True):
            sleep(5)
            try:
                # Choosing arbitrary percentage to keep the lease alive.
                lease.HttpNfcLeaseProgress(50)
                if (lease.state == vim.HttpNfcLease.State.done):
                    return
                    # If the lease is released, we get an exception.
                    # Returning to kill the thread.
            except:
                return

    def get_ovf_descriptor(self, ovf_file):
        """
        Read in the OVF descriptor.
        """
        try:
            ovfd = ovf_file.read()
            return ovfd
        except:
            logger.info("Could not read file: %s" % ovf_file)
            raise RuntimeError('Could not read file: %s" % ovf_file')

    def get_obj_in_list(self, obj_name, obj_list):
        """
        Gets an object out of a list (obj_list) whos name matches obj_name.
        """
        for o in obj_list:
            if o.name == obj_name:
                return o
        logger.info("Unable to find object by the name of %s in list:\n%s" %
                    (o.name, map(lambda o: o.name, obj_list)))
        raise RuntimeError('Couldnt find the object')

    def mark_vm_as_template(self, vm_name):
        if (not vm_name) or (not str(vm_name).strip()):
            raise ValueError("virtual machine name - invalid value or type")
        logger.info('Converting vm {} to template'.format(vm_name))
        vm_obj = self._get_obj([vim.VirtualMachine], vm_name)
        if vm_obj.config.template:
            logger.info('VM is already a template so skipping')
            return
        try:
            vm_obj.MarkAsTemplate()
        except Exception as e:
            raise RuntimeError('Failed to convert to template- Error- {}'.format(e))

    def get_objects(self, si, **kwargs):
        """
        Return a dict containing the necessary objects for deployment.
        """
        # Get datacenter object.
        datacenter_list = si.content.rootFolder.childEntity
        if kwargs.has_key('datacenter_name'):
            datacenter_obj = self.get_obj_in_list(kwargs['datacenter_name'], datacenter_list)
        else:
            datacenter_obj = datacenter_list[0]

        # Get datastore object.
        datastore_list = datacenter_obj.datastoreFolder.childEntity
        if kwargs.has_key('datastore_name'):
            datastore_obj = self.get_obj_in_list(kwargs['datastore_name'], datastore_list)
        elif len(datastore_list) > 0:
            datastore_obj = datastore_list[0]
        else:
            logger.info("No datastores found in DC (%s)." % datacenter_obj.name)

        # Get cluster object.
        cluster_list = datacenter_obj.hostFolder.childEntity
        if kwargs.has_key('cluster_name'):
            cluster_obj = self.get_obj_in_list(kwargs['cluster_name'], cluster_list)
        elif len(cluster_list) > 0:
            cluster_obj = cluster_list[0]
        else:
            logger.info("No clusters found in DC (%s)." % datacenter_obj.name)

        # Generate resource pool.
        resource_pool_obj = cluster_obj.resourcePool

        return {"datacenter": datacenter_obj,
                "datastore": datastore_obj,
                "resource pool": resource_pool_obj
                }

    def deploy_ova_on_vcenter(self, ova_path, **kwargs):
        """
        :param ova_path: path to ova or ovf
        :param kwargs: kwargs contain datacenter name, datastore and cluster name
        :return:
        """
        si = self.vCenter_cre_dict['si']
        ova = True
        # Get the input format and get the file size and ovf object
        if ova_path.endswith('ova'):
            logger.info('Provided input is of type ova')
            t = tarfile.open(ova_path)
            folder_files = t.getnames()
            ovffilename = list(filter(lambda x: x.endswith(".ovf"), folder_files))[0]
            ovffile = t.extractfile(ovffilename)
        elif os.path.isdir(ova_path):
            logger.info('Provided input is of type ovf')
            folder_files = os.listdir(ova_path)
            ovffilename = list(filter(lambda x: x.endswith(".ovf"), folder_files))[0]
            xx = os.path.join(ova_path, ovffilename)
            ovffile = open(xx, 'r')
            ova = False
        else:
            raise RuntimeError('Wrong ova file type - {}'.format(ova_path))
        ovfd = self.get_ovf_descriptor(ovffile)
        ovffile.close()
        objs = self.get_objects(si, **kwargs)
        manager = si.content.ovfManager
        # The below commented code is to handle the network name for ovf/ova deployment
        # parsparms = vim.OvfManager.ParseDescriptorParams()
        # res_des = si.content.ovfManager.ParseDescriptor(ovfd, parsparms)
        # network_map = vim.OvfManager.NetworkMapping()
        # network_map.name = res_des.network.name
        # network_map.network = objs["network"]
        # spec_params = vim.OvfManager.CreateImportSpecParams(networkMapping=[network_map])
        spec_params = vim.OvfManager.CreateImportSpecParams(entityName=kwargs['entityName'])
        import_spec = manager.CreateImportSpec(ovfd,
                                               objs["resource pool"],
                                               objs["datastore"],
                                               spec_params)
        # Not printing the warnings
        # if len(import_spec.warning) > 0:
        #     logger.warn("Warnings during processing: %s" % import_spec.warning)
        if len(import_spec.error) > 0:
            logger.error("Errors during processing: %s" % import_spec.error)
            raise RuntimeError("Errors during processing: %s" % import_spec.error)
        if import_spec.importSpec is None:
            print("Spec is empty, cannot continue")
            raise RuntimeError("Spec is empty, cannot continue")
        lease = objs["resource pool"].ImportVApp(import_spec.importSpec,
                                                 objs["datacenter"].vmFolder)
        while True:
            if lease.state == vim.HttpNfcLease.State.ready:
                # Spawn a dawmon thread to keep the lease active while POSTing
                # VMDK.
                keepalive_thread = Thread(target=self.keep_lease_alive, args=(lease,))
                keepalive_thread.start()

                for deviceUrl in lease.info.deviceUrl:
                    url = deviceUrl.url.replace('*', self.vCenter_cre_dict["host"])
                    fileItem = list(filter(lambda x: x.deviceId ==
                                                     deviceUrl.importKey,
                                           import_spec.fileItem))[0]
                    ovffilename = list(filter(lambda x: x == fileItem.path,
                                              folder_files))[0]
                    ovffile = \
                        t.extractfile(ovffilename) if ova else open(os.path.join(ova_path, ovffilename), 'r')
                    size_of_file = \
                        t.extractfile(ovffilename).size if ova else os.path.getsize(os.path.join(ova_path, ovffilename))
                    headers = {'Content-length': size_of_file}
                    req = urllib2.Request(url, ovffile, headers)
                    try:
                        response = urllib2.urlopen(req)
                    except httplib.BadStatusLine:
                        continue
                lease.HttpNfcLeaseComplete()
                keepalive_thread.join()
                return 0
            elif lease.state == vim.HttpNfcLease.State.error:
                logger.error("Lease error: %s" % lease.error)
                raise RuntimeError("Lease error: %s" % lease.error)
        connect.Disconnect(si)

    def import_custom_spec(self, spec_name, spec_path):
        """
        This code imports custo specification with spec name
        :param spec_name: Custom spec name
        :param spec_path: Path to custom spec
        :return:
        """
        si = self.vCenter_cre_dict['si']
        spec_fh = open(spec_path, 'r')
        spec_xml = spec_fh.read()
        spec_fh.close()
        spec_manager = si.content.customizationSpecManager
        if spec_manager.DoesCustomizationSpecExist(spec_name):
            logger.info('Specifiaction name {} already exists'.format(spec_name))
            return
        try:
            spec = spec_manager.XmlToCustomizationSpecItem(specItemXml=spec_xml)
            spec.info.name = spec_name
            logger.info('Importing specification {}'.format(spec.info.name))
            spec_manager.CreateCustomizationSpec(spec)
        except Exception as e:
            logger.error('Importing custom spec failed with error -{er}'.format(er=e))
            raise RuntimeError('Importing custom spec failed with error -{er}'.format(er=e))

        logger.info('Successfully imported custom spec')

    def get_datacenter_moid(self,datacenter):
        datacenterobj =  self._get_obj([vim.Datacenter],
                                       datacenter)
        return datacenterobj

    def get_datastore_id(self,datastore):
        datastoreobj = self._get_obj([vim.Datastore],
                                     datastore)
        return datastoreobj

    def get_portgroup_id(self ,portgroup):
        portgrpobj = self._get_obj([vim.DistributedVirtualPortgroup],
                                   portgroup)
        return portgrpobj

    def get_folder_id(self,folder_name):
        folderobj = self._get_obj([vim.Folder],folder_name)
        return folderobj

    def get_host_id(self,host_name):
        folderobj = self._get_obj([vim.HostSystem],host_name)
        return folderobj
