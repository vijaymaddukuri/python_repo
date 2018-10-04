#  Copyright 2016 EMC GSE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pyVmomi import vim
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect
import ssl
import atexit
from requests.packages import urllib3


class vSphereValidation(object):
    def __init__(self, hostaddress, username, password, port=443):

        if (not hostaddress) or (not str(hostaddress).strip()):
            raise ValueError("vCenter name - invalid value or type")
        if (not username) or (not str(username).strip()):
            raise ValueError("vCenter username - invalid value or type")
        if (not password) or (not str(password).strip()):
            raise ValueError("vCenter password - invalid value or type")
        if (not port) or (not str(port).strip()):
            port = 443
        elif str(port).strip().isdigit():
            port = int(str(port).strip())

        context = None
        # Disabling urllib3 ssl warnings
        urllib3.disable_warnings()

        # Disabling SSL certificate verification
        if hasattr(ssl, 'SSLContext'):
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.verify_mode = ssl.CERT_NONE

        try:
            if context:
                self.si = SmartConnect(host=hostaddress, user=username, pwd=password, port=port, sslContext=context)
            else:
                self.si = SmartConnect(host=hostaddress, user=username, pwd=password, port=port)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

        if not self.si:
            raise RuntimeError("Unable to connect {vCenter} using credential "
                               "{username}/{password}!".format(vCenter=hostaddress,
                                                               usernme=username,
                                                               password=password))
        atexit.register(Disconnect, self.si)
        self.content = self.si.RetrieveContent()

    def verify_VM_not_exist_in_vCenter(self, vm_name):
        """
        Verify whether the vm exists in vCenter or not
        :param: vm_name The given text name of the vm
        :return: True or raise error
        """
        if (not vm_name) or (not str(vm_name).strip()):
            raise ValueError("virtual machine name - invalid value or type")
        vm_obj = self._get_obj([vim.VirtualMachine], vm_name)
        if vm_obj:
            return False
        else:
            return True

    def verify_Folder_not_exist_in_vCenter(self, folder_name):
        """
        Verify whether the folder exists in vCenter or not
        :param folder_name: The given text name of the folder
        :return: True or raise error
        """
        if (not folder_name) or (not str(folder_name).strip()):
            raise ValueError("virtual machine name - invalid value or type")
        folder_obj = self._get_obj([vim.Folder], folder_name)
        if folder_obj:
            return False
        else:
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
        container = self.content.viewManager.CreateContainerView(self.content.rootFolder, vim_type, True)
        for c in container.view:
            if c.name == vm_name:
                obj = c
                break
        return obj

    def __close_connect(self):
        """
        Close current connection with vCenter
        """
        if self.si:
            connect.Disconnect(self.si)
            self.si = None
            self.content = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close_connect()
