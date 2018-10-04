from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

import argparse
import atexit
import getpass
import ssl

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(
       description='Process args for retrieving all the Virtual Machines')
   parser.add_argument('-s', '--host', required=True, action='store',
                       help='Remote host to connect to')
   parser.add_argument('-o', '--port', type=int, default=443, action='store',
                       help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store',
                       help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=False, action='store',
                       help='Password to use when connecting to host')
   args = parser.parse_args()
   return args


def print_vm_info(virtual_machine, vm_name):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary

    if summary.config.name==vm_name:
        print(summary)
        print("Name       : ", summary.config.name)
        print("Template   : ", summary.config.template)
        print("Path       : ", summary.config.vmPathName)
        print("Guest      : ", summary.config.guestFullName)
        print("Instance UUID : ", summary.config.instanceUuid)
        print("Bios UUID     : ", summary.config.uuid)
        annotation = summary.config.annotation
        if annotation:
            print("Annotation : ", annotation)
        print("State      : ", summary.runtime.powerState)
        if summary.guest is not None:
            ip_address = summary.guest.ipAddress
            tools_version = summary.guest.toolsStatus
            if tools_version is not None:
                print("VMware-tools: ", tools_version)
            else:
                print("Vmware-tools: None")
            if ip_address:
                print("IP         : ", ip_address)
            else:
                print("IP         : None")
        if summary.runtime.question is not None:
            print("Question  : ", summary.runtime.question.text)
        print("")
        return {'instance_id': summary.config.instanceUuid, 'bios_id': summary.config.uuid}

def main():
   """
   Simple command-line program for listing the virtual machines on a system.
   """

   args = GetArgs()
   if args.password:
      password = args.password
   else:
      password = getpass.getpass(prompt='Enter password for host %s and '
                                        'user %s: ' % (args.host,args.user))

   context = None
   if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()
   service_instance = SmartConnectNoSSL(host=args.host,
                     user=args.user,
                     pwd=password,
                     port=int(args.port))
   atexit.register(Disconnect, service_instance)

   content = service_instance.RetrieveContent()

   container = content.rootFolder  # starting point to look into
   viewType = [vim.VirtualMachine]  # object types to look for
   recursive = True  # whether we should look into it recursively
   containerView = content.viewManager.CreateContainerView(
       container, viewType, recursive)

   children = containerView.view
   id_dict={}
   for child in children:
       # id_dict= print_vm_info(child, 'demo_vj')
       summary = child.summary
       if summary.config.name == 'demo_vj':
           return summary.config.instanceUuid

# Start program
if __name__ == "__main__":
    main()