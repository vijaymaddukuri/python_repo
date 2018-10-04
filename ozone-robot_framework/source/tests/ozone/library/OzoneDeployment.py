# -*- coding: utf-8 -*-
from ozoneConstants import OSType, REMOTE_SHELL_PATH
import ozoneConstants as constants
from common import vCenterOps
from robot.api import logger
from pyVmomi import vim
import os
import time
from common import vmUtils
from common.pyvmomiUtil import runScript, getVSphereObj, uploadFileToVM, makeGuestOSAuthentication, connectToVcenter, \
    getVAppByName, disconnectFromVcenter
from cifsUtil import CIFS


class Ozone(object):
    def __init__(self, vCenterDict):
        """
            Description: This function deploys Ozone vApp manager
            :param vCenterDict (DICT)
                    vCenterDict[vCenterIPAddress] – vCenter Server FQDN (STRING)
                    vCenterDict[vCenterUsername] - vCenter server user name (STRING)
                    vCenterDict[vCenterPassword] - vCenter server password (STRING)
                    vCenterDict[vCenterPort] - vCenter server port (INT)

        """
        try:
            self.service_instance = connectToVcenter(vCenterHost=vCenterDict['host'],
                                                     username=vCenterDict['username'],
                                                     password=vCenterDict['password'],
                                                     portNum=vCenterDict['portNum'])
        except Exception as err:
            logger.error("Unable to Login to the vCenter")
            logger.error(err.message)

    def get_datastore(self, dsname):
        """
        Description:
        :param serviceInstance: vCenter service instance (OBJECT)
        :param dsname: Datastorename
        :return    ds: datastore Name
        """
        for dc in self.service_instance.content.rootFolder.childEntity:
            for ds in dc.datastore:
                if ds.name == dsname:
                    return True
        return False

    def checkDeployEnv(self, vCenterDict, ovfDict):
        """
                Description: This function checks whether the deploy environment is well or not
                :param vCenterDict (DICT)
                    vCenterDict[vCenterIPAddress] – vCenter Server FQDN (STRING)
                    vCenterDict[vCenterUsername] - vCenter server user name (STRING)
                    vCenterDict[vCenterPassword] - vCenter server password (STRING)
                    vCenterDict[hostName] - ESXi host IP address or the DNS name (STRING)
                    vCenterDict[datastore] - Name of datastore (STRING)
                    vCenterDict[cluster] - Name of cluster (STRING)
                    vCenterDict[dataCenter] – Name of datacentre (STRING)
                :param ovfDict (DICT)
                    ovfDict[vmNetwork] – Network(Port Group)(STRING)
                :returns True/False, Error message
        """

        content = self.service_instance.RetrieveContent()

        # Check Cluster
        clusterObj = getVSphereObj(content,
                                   [vim.ClusterComputeResource],
                                   vCenterDict['cluster'])
        if not clusterObj:
            return False, 'Cluster {} is not found'.format(vCenterDict['cluster'])
        # Check ESXi Host
        if vCenterDict['hostName']:
            esxiHostObj = getVSphereObj(content,
                                        [vim.HostSystem],
                                        vCenterDict['hostName'])
            if not esxiHostObj:
                return False, 'ESXi host {} is not found'.format(vCenterDict['hostName'])
        # Check Datastore
        datastoreObj = self.get_datastore(vCenterDict['datastore'])
        if not datastoreObj:
            return False, 'datastore {} is not found'.format(vCenterDict['datastore'])
        # Check Port Group, standard switch network
        portGroup = getVSphereObj(content,
                                  [vim.Network],
                                  ovfDict['network'])
        if not portGroup:
            return False, 'Network {} is not found'.format(ovfDict['vmNetwork'])

        return True, None

    def waitForRestService(self, ipaddress):
        """
        Description : Wait till the REST Service is Up on the machine
        :param ipaddress: Ozone Master ipaddres
        :return: True or False
        """
        import requests
        url = 'https://{}:443'.format(ipaddress)
        counter = 0
        while True and counter < 10:
            response = requests.get(url, verify=False)
            time.sleep(30)
            if response.status_code == 200:
                logger.info('REST Service is Running ')
                return True
            else:
                counter += 1
        return False

    def deployOzonevApp(self, vCenterDict, ovfDict, timeout=constants.OVA_DEPLOY_TIMEOUT):
        """
            Description: This function deploys Ozone vApp manager
            :param vCenterDict (DICT)
                    vCenterDict[vCenterIPAddress] – vCenter Server FQDN (STRING)
                    vCenterDict[vCenterUsername] - vCenter server user name (STRING)
                    vCenterDict[vCenterPassword] - vCenter server password (STRING)
                    vCenterDict[vCenterPort] - vCenter server port (INT)
                    vCenterDict[dataCenter] – Name of datacenter (STRING)
                    vCenterDict[cluster] - Name of cluster (STRING)
                    vCenterDict[hostName] - ESXi host IP address or the DNS name (STRING)
                    vCenterDict[datastore] - Name of datastore (STRING)
                    vCenterDict[resourcePool] - Name of resource pool (STRING) (OPTIONAL)
            :param ovfDict (DICT)
                    ovfDict[ovaPath] – Full absolute path of the OVA file (STRING)
                    ovfDict[vmName] – Name of Ozone vApp (STRING)
                    ovfDict[network] – Network(Port Group) of the Ozone vApp (STRING)
                    ovfDict[masterIP] – Ozone vApp master ip(STRING)
                    ovfDict[masterFQDN] – Ozone vApp master fqdn (STRING)
                    ovfDict[workerIP] – Ozone vApp worker ip (STRING)
                    ovfDict[workerFQDN] – Ozone vApp worker fqdn (STRING)
                    ovfDict[gateway] – DNS Server(STRING)
                    ovfDict[netmask] – netmask(STRING)
                    ovfDict[dns] – DNS Server(STRING)
            :param timeout - Time Out(Second) for deploy the OVA File (INT)(Optional)
            :return True/False
            """
        # Check the environment first
        envStatus, err = self.checkDeployEnv(vCenterDict, ovfDict)
        if not envStatus:
            logger.error(err)
            return False

        # Dictionary for VM data to be deployed
        vmData = {
            'vmName': ovfDict['vmName'],
            'powerState': 'ON',
            'diskStorageFormat': "thin"
        }

        ovfConfigDict = {
            'masterIP': ovfDict['masterIP'],
            'masterFQDN': ovfDict['masterFQDN'],
            'workerIP': ovfDict['workerIP'],
            'workerFQDN': ovfDict['workerFQDN'],
            'gateway': ovfDict['gateway'],
            'netmask': ovfDict['netmask'],
            'dns': ovfDict['dns'],
            'network': ovfDict['network'],
            'ipPolicy': "fixedPolicy",
            'ipProtocol': "IPv4"
        }
        ovaDetails = {'type': 'Ozone',
                      'ovaSource': ovfDict['ovaPath'],
                      'ovfConfigDict': ovfConfigDict,
                      'IsvApp': True
                      }

        try:
            vCenterOps.deployOVA(vCenterData=vCenterDict,
                                 vmData=vmData,
                                 ovaDetails=ovaDetails,
                                 timeout=timeout)
            self.waitForRestService(ovfConfigDict['masterIP'])
            return True
        except Exception as err:
            logger.error("Exception while deploying Ozone ova.")
            logger.error(err.message)
            return False

    def download_Latest_Ozone(self, cifs_details, remote_filepath,
                              local_filepath,
                              prefix, suffix):
        """
        Description: Method to download Latest ova from CIFS share
        :param cifs_details: 
            cifs_detailsp['ipaddrss']
        :param remote_filepath: 
        :param local_filepath: 
        :param prefix: 
        :param suffix: 
        :return: 
        """
        cifs = CIFS(username=cifs_details['username'], password=cifs_details['password'],
                    serverIP=cifs_details['ip_address'], port=cifs_details['port'])
        fileList = cifs.listFile(remote_filepath)
        begin = len(prefix)
        end = len(suffix)
        versionList = []
        for file in fileList:
            if file.startswith(prefix):
                version = file[begin:-end]
                if len(version) == 3:
                    versionList.append(version)
        versionList.sort()
        ovaFileName = '{0}{1}{2}'.format(prefix, versionList[-1], suffix)
        remoteLatestOzonePath = '{0}{1}'.format(remote_filepath, ovaFileName)
        os.mkdir(local_filepath)
        localOzoneFilePath = '{0}{1}'.format(local_filepath, ovaFileName)
        assert cifs.download(localFilePath=localOzoneFilePath, remoteFilePath=remoteLatestOzonePath)

    def destroyVapp(self, vCenterDict, vappName, timeout=300):
        """
            Description: destroy the vApp in vCenter
           :param vCenterDict: Dictionary:
                 'host' - vCenter Hostname
                 'username' - username for vCenter
                 'password' - password for vCenter
           :param vApp Name(String)
           :return: True or False
        """
        try:
            vapp = getVAppByName(self.service_instance, vappName)
            if not vapp:
                return False
            # If the vApp power on,Power off it and set the timeout in the shutdown of the process
            if vapp.summary.vAppState == vim.VirtualApp.VAppState.started:
                task = vapp.PowerOff(True)
                timecount = 0
                while True:
                    state = task.info.state
                    if state == vim.TaskInfo.State.success:
                        logger.info("{} has been powered off successfully".format(vapp.name))
                        break
                    elif state == vim.TaskInfo.State.error:
                        logger.info("{} does not been powered off".format(vapp.name))
                        return False
                    time.sleep(5)
                    timecount += 5
                    if timecount > timeout:
                        task.CancelTask()
                        break
            vapp.Destroy()
            logger.info("vApp %s has been destroyed successfully" % vappName)
            return True
        except Exception as err:
            logger.error("Exception while destroying vApp")
            logger.error(err.message)
            return False

    @staticmethod
    def pickupLatestOzoneOva(path, prefix, suffix):
        """
            Description: This function deploys Ozone vApp manager
            :param path - Ozone ova file path(String)
            :param prefix - Ozone ova file prefix(String)
            :param suffix - Ozone ova file suffix(String)
            :return Latest Ozone ova file path
            """
        try:
            logger.info('Begin to get latest Ozone vApp')
            fileList = os.listdir(path)
            begin = len(prefix)
            end = len(suffix)
            versionList = []
            for file in fileList:
                if file.startswith(prefix):
                    version = file[begin:-end]
                    if len(version) == 3:
                        versionList.append(version)
            versionList.sort()
            latestOzone = '{0}{1}{2}{3}'.format(path, prefix, versionList[-1], suffix)
            logger.info('Latest Ozone ova path is %s' % latestOzone)
            return latestOzone
        except Exception as err:
            logger.error("Exception while picking up latest Ozone ova.")
            logger.error(err.message)

    def checkServiceStatus(self, filepath):
        """
        Description: Reads the file and return a boolean
        Parameters : filePath - The path of the to be read (STRING)
        Returns: True or False
        """
        with open(filepath, 'r') as inFile:
            data = inFile.read()
            return constants.SUCCESS_MESSAGE_AGENT in data

    def configAgent(self, vCenterDict, vmDict):
        '''
        Description: This function configure Agent in vm
        :param : vCenterDict - vCenter info(DICTIONARY)
                         vCenterDict["host"] - vCenter IP(STRING)
                         vCenterDict["user"] - User name for vCenter(STRING)
                         vCenterDict["password"] - Password for vCenter(STRING)
                 vmDict - appliance VM info(DICTIONARY)
                         vmDict["vmname"] - Guest VM Name(STRING)
                         vmDict["vmusername"] - Guest VM name(STRING)
                         vmDict["vmpassword"] - Guest VM Password(STRING)
                         vmDict["datacenter"] - the datacenter to the VM location (STRING)
                         vmDict["folderPath"] - the folder path to the VM location, e.g. '/Project1/cycle1/' or 'Project1/cycle1' (STRING)
                         vmDict["vappname"] - The vApp name (STRING)
        :return True/False
        '''

        try:
            # Get VAPP object then get the vm object
            logger.info('Start to retrieve vapp object by inventory path: \n \
                         datacenter: %s, folder path: %s, vm name: %s' % (
                vmDict['datacenter'], vmDict['folderPath'], vmDict['vappname']))
            vCenterDict['user'] = vCenterDict['username']
            vapp = vmUtils.findvAppByInventoryPath(vCenterDict,
                                                   vmDict['datacenter'],
                                                   vmDict['vappname'],
                                                   vmDict['folderPath'])
            logger.info('Successfully get target vapp %s object' % vmDict['vappname'])

            vm = filter(lambda vm: vm.name == vmDict['vmname'], vapp.vm)[0]

            if vm:
                logger.info('Successfully get target vm %s object' % vmDict['vmname'])
            else:
                logger.error('Could not get vm object by path: %s/%s in vCenter %s' % (
                    vmDict['folderPath'],
                    vmDict['vmname'],
                    vCenterDict['host']))
                raise

            # Create vm guest os auth
            cred = makeGuestOSAuthentication(vmDict['vmusername'], vmDict['vmpassword'])
            logger.info('Create vm guest os auth for user %s' % vmDict['vmusername'])

            # GuestOSType init
            guestOSType = OSType.WINDOWS

            # get local file path
            localFilename = os.path.join(os.path.dirname(__file__),
                                         constants.FILE_NAME)
            logger.info('Local file for uploading to vm: %s' % localFilename)

            # Remote file path
            remoteFilename = constants.REMOTE_FILE_PATH
            logger.info('File path of target VM is: %s' % remoteFilename)

            # Upload the BAT file to target vm os
            logger.info('Start to upload BAT file: %s to target vm: %s' % (
                constants.FILE_NAME,
                vmDict['vmname']))

            filepath = uploadFileToVM(self.service_instance, vm, cred, localFilename, guestOSType,
                                      remoteFilename)
            if filepath:
                logger.info('Successfully upload BAT file to target vm: %s, on vCenter: %s' % (
                    vmDict['vmname'],
                    vCenterDict['host']))

            else:
                logger.error('Fail to upload BAT file to VM %s' % vmDict['vmname'])

            # get the scriptdict
            scriptDict = {}
            scriptDict['localScriptPath'] = "{0}{1}configAgent.ps1". \
                format(os.path.dirname(os.path.abspath(__file__)), os.path.sep)

            logger.info("Begin to run script: %s" % scriptDict['localScriptPath'])

            scriptDict['remoteShellPath'] = REMOTE_SHELL_PATH[guestOSType]['shell']
            logger.info("Remote shell path of server %s is %s" % (vmDict['vmname'], scriptDict['remoteShellPath']))
            scriptDict['timeout'] = 120

            # run the script of bat file to configure
            exitCode, outFilePath = runScript(self.service_instance, vm, cred, guestOSType, scriptDict)
            if exitCode != 0:
                logger.error("Failed to configure agent")
                return False

            if self.checkServiceStatus(outFilePath):
                logger.info("Complete to validate the configure agent")
                return True
            else:
                logger.info("Failed to validate the configure agent")
                return False


        except Exception as exc:
            logger.error('Fail to configure Agent')
            logger.error(exc)

    @staticmethod
    def delete_file_folder(src):
        '''delete files and folders'''
        if os.path.isfile(src):
            try:
                os.remove(src)
                logger.info("%s is removed" % src)
            except:
                pass
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc = os.path.join(src, item)
                Ozone.delete_file_folder(itemsrc)
            try:
                os.rmdir(src)
                logger.info("%s is removed" % src)
            except:
                pass