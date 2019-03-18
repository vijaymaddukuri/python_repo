item = {'HardwareTemplateID': 'a66e0d2a-587e-4bd0-9802-853b2c75185d', 'CustomerDefinedName': 'sheetal_vm2', 'TenantID': '9f92203e-313c-4b35-88ff-ff00a9d77153', 'SourceTemplateID': '3e98b32d-213e-487a-a414-66b34fbc9aa8', 'Nics': [{'Connected': 'false', 'ipAddressMode': '1', 'isNotPoweredOn': 'false', 'NetworkIdentifier': 'network-56', 'MacAddress': '00:50:56:84:c9:c6', 'customerDefinedName': 'dvPortGroup-test', 'AdapterType': '4', 'ipTextToShow': 'DHCP', 'VirtualMachineNicID': 'f012fe61-b3a3-fe19-2f1d-3d59a587893b', 'NetworkID': '6ae7f8c6-0b68-abb8-185b-c84926f7d279', 'ipAddress': '', 'DeviceKey': '4000', 'disableNICTypeEdit': 'true'}], 'Hypervisor': {'Site': {'SiteID': '69d29e4b-ce66-66b9-a07d-c4612616bb0f'}}, 'Disks': [{'StorageID': '44739f0e-3dca-114d-5b33-d6229c00dd01', 'VirtualMachineDiskID': '2076012e-5aad-7672-6efd-b9cf510d28e2', 'ControllerBusNumber': '0', 'StorageIdentifier': 'datastore-12', 'computeAllocationID': 'ca6f9e10-51b1-c33a-6225-3bcb2402294c', 'capacity': '0', 'FreeSpaceKB': 'null', 'DiskFileName': '[5TBDatastore] vec-he_template/vec-he_template.vmdk', 'DeviceKey': '2000', 'freeSpaceUnit': '', 'StorageProfileID': '40aee1c1-13a9-46ea-81c7-ca91e7f96247', 'DiskMode': '5', 'CapacityKB': '62914560', 'capacityUnit': '', 'freeSpace': '0', 'scsiLabel': 'SCSI 0', 'StorageProfileName': 'LAB - Tier II Block Storage - LOCAL', 'DiskNumber': '1', 'UnitNumber': '0'}], 'ComputeProfileID': '4f44c852-1a0b-4343-8f22-6ba6d52e1263'}

yaml_res = '''
vm_template:
	CustomerDefinedName: sheetal_vm2
	SourceTemplateID: 3e98b32d-213e-487a-a414-66b34fbc9aa8
	Hypervisor:
	  Site:
		SiteID: 69d29e4b-ce66-66b9-a07d-c4612616bb0f
	HardwareTemplateID: a66e0d2a-587e-4bd0-9802-853b2c75185d
	Nics:
	- disableNICTypeEdit: 'true'
	  customerDefinedName: dvPortGroup-test
	  DeviceKey: '4000'
	  VirtualMachineNicID: f012fe61-b3a3-fe19-2f1d-3d59a587893b
	  AdapterType: '4'
	  NetworkID: 6ae7f8c6-0b68-abb8-185b-c84926f7d279
	  MacAddress: 00:50:56:84:c9:c6
	  ipTextToShow: DHCP
	  ipAddressMode: '1'
	  isNotPoweredOn: 'false'
	  Connected: 'false'
	  NetworkIdentifier: network-56
	  ipAddress: ''
	Disks:
	- freeSpace: '0'
	  ControllerBusNumber: '0'
	  VirtualMachineDiskID: 2076012e-5aad-7672-6efd-b9cf510d28e2
	  StorageProfileID: 40aee1c1-13a9-46ea-81c7-ca91e7f96247
	  DiskMode: '5'
	  StorageProfileName: LAB - Tier II Block Storage - LOCAL
	  scsiLabel: SCSI 0
	  DiskNumber: '1'
	  DiskFileName: "[5TBDatastore] vec-he_template/vec-he_template.vmdk"
	  capacityUnit: ''
	  freeSpaceUnit: ''
	  FreeSpaceKB: 'null'
	  computeAllocationID: ca6f9e10-51b1-c33a-6225-3bcb2402294c
	  DeviceKey: '2000'
	  UnitNumber: '0'
	  StorageID: 44739f0e-3dca-114d-5b33-d6229c00dd01
	  CapacityKB: '62914560'
	  capacity: '0'
	  StorageIdentifier: datastore-12
	ComputeProfileID: 4f44c852-1a0b-4343-8f22-6ba6d52e1263
	TenantID: 9f92203e-313c-4b35-88ff-ff00a9d77153
'''

import yaml
import json
import os

with open(r'C:\Users\madduv\Desktop\profile.conf', 'r') as yml:
    print(type(yml))
    output = yaml.load(yml)
    print(output)
    new = json.dumps(output['xstream-centos']['vm_template'])
print(new)