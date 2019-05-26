from mock import MagicMock
from mock import patch
import unittest
from backup.Networker import Networker
from common.exceptions import TASException


def side_effect_resource(value1, value2, value3):
    testnetworker = TestNetworker()
    if value1 == 'GET' and value2 == "/nwrestapi/v2/global/clients":
        return testnetworker.mock_clients()
    elif value1 == 'GET' and value2 == "/nwrestapi/v2/global/jobs":
        return testnetworker.mock_jobs_reponse()
    else:
        return {}


class TestNetworker(unittest.TestCase):
    """
    This Class Tests all the functionalities of the Networker Class
    """
    pause_input_data = { 'hostname': 'rhel72',
                              'resourceId': { 'sequence': 4,
                                              'id': '12.10.100.249.48'
                                              }
                              }
    @patch('backup.Networker.RestApiTemplate')
    def test_get_all_clients(self, request_mock):
        instance = request_mock.return_value
        instance.send_request.return_value = self.mock_clients()
        self.networker = Networker("username", "password", "url")

        result = self.networker.get_all_clients()
        self.assertEqual(result, self.mock_clients())
        
    @patch('backup.Networker.RestApiTemplate')
    def test_get_client(self, request_mock):
        instance = request_mock.return_value
        instance.send_request.return_value = {}
        self.networker = Networker("username", "password", "url")
        
        result = self.networker.get_client("100")
        self.assertEqual(result, {})

    @patch('backup.Networker.RestApiTemplate')
    def test_get_client_resource_id(self, request_mock):
        instance = request_mock.return_value
        instance.send_request.return_value = self.mock_clients()
        self.networker = Networker("username", "password", "url")
        
        result = self.networker.get_client_resource_id("nve-1.7.xstest.local")
        self.assertEqual(result, "82.0.227.11.0.0.0.0.90.46.88.91.10.100.249.48")
        

    @patch('backup.Networker.RestApiTemplate')
    def test_get_protection_group(self, request_mock):
        instance = request_mock.return_value
        instance.send_request.return_value = {}
        self.networker = Networker("username", "password", "url")
        
        result = self.networker.get_protection_group("Bronze-Filesystem")
        self.assertEqual(result, {})
    

    @patch('backup.Networker.RestApiTemplate')
    @patch('backup.Networker.Networker.get_protection_group')
    def test_add_client_to_protection_group(self, pg_mock, request_mock):
        pg_mock.return_value = self.mock_pg()
        instance = request_mock.return_value
        instance.send_request.return_value = 204
        self.networker = Networker("username", "password", "url")
    
        result = self.networker.add_client_to_protection_group("Bronze-Filesystem-new", self.mock_client())
        self.assertEqual(result, 204)


    @patch('backup.Networker.RestApiTemplate')
    def test_get_backup_history_of_client(self, request_mock):
        instance = request_mock.return_value
        instance.send_request.return_value = {}
        self.networker = Networker("username", "password", "url")

        result = self.networker.get_backup_history_of_client("rid")
        self.assertEqual(result, {})
    
    
    @patch('backup.Networker.RestApiTemplate')
    @patch('backup.Networker.Networker.get_protection_group')
    def test_remove_client_from_protection_group(self, pg_mock, request_mock):
        pg_mock.return_value = self.mock_pg()
        instance = request_mock.return_value
        instance.send_request.return_value = 204
        self.networker = Networker("username", "password", "url")

        result = self.networker.remove_client_from_protection_group("47.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48", "Bronze-Filesystem")
        self.assertEqual(result, 204)
    
    @patch('backup.Networker.RestApiTemplate')
    def test_delete_client(self, request_mock):
        instance = request_mock.return_value
        instance.send_request.return_value = 204
        self.networker = Networker("username", "password", "url")

        result = self.networker.delete_client("rid")
        self.assertEqual(result, 204)

    @patch('backup.Networker.RestApiTemplate')
    def test_is_full_exceed_client_limit(self, request_mock):
        instance = request_mock.return_value
        instance.send_request.return_value = self.mock_clients()
        self.networker = Networker("username", "password", "url")
        result = self.networker.is_full(3,1)
        self.assertTrue(result, True)

        #client dictionary doesn't have count variable
        instance.send_request.return_value = self.mock_client()
        result = self.networker.is_full(3,1)
        self.assertTrue(result, True)

    @patch('backup.Networker.RestApiTemplate.send_request', side_effect=side_effect_resource)
    def test_is_full_exceed_job_limit(self, request_mock):
        self.networker = Networker("username", "password", "url")
        result = self.networker.is_full(4,1)
        self.assertTrue(result, True)

    @patch('backup.Networker.RestApiTemplate.send_request', side_effect=side_effect_resource)
    def test_is_full_within_limit(self, request_mock):
        self.networker = Networker("username", "password", "url")
        result = self.networker.is_full(4,2)
        self.assertFalse(result, False)

    @patch('backup.Networker.Networker.get_client')
    @patch('backup.Networker.Networker.get_client_resource_id')
    @patch('backup.Networker.Networker.add_client_to_protection_group')
    def test_enable_backup_positive(self, add_client_mock, client_rid_mock, client_mock):
        client_mock.return_value = self.mock_client()
        client_rid_mock.return_value = "82.0.227.11.0.0.0.0.90.46.88.91.10.100.249.48"
        add_client_mock.return_value = "204"
        self.networker = Networker("username", "password", "url")

        result = self.networker.enable_backup("dummy", ["All"], "Bronze-Filesystem")
        self.assertEqual(result, self.mock_enable_success())


    @patch('backup.Networker.Networker.get_client')
    @patch('backup.Networker.Networker.get_client_resource_id')
    @patch('backup.Networker.Networker.add_client_to_protection_group')
    def test_enable_backup_get_error(self, add_client_mock, client_rid_mock, client_mock):
        client_mock.return_value = self.mock_error()
        client_rid_mock.return_value = "82.0.227.11.0.0.0.0.90.46.88.91.10.100.249.48"
        add_client_mock.return_value = "204"
        self.networker = Networker("username", "password", "url")

        result = self.networker.enable_backup("dummy", ["All"], "Bronze-Filesystem")
        self.assertEqual(result, self.mock_enable_error())
    
    @patch('backup.Networker.RestApiTemplate')
    def test_change_backup_state_invalid_input(self, request_mock):
        instance = request_mock.return_value
        mock_response_put_positive = '<Response [204]>'
        instance.send_request.return_value = mock_response_put_positive
        self.networker = Networker("username", "password", "url")
        with self.assertRaises(Exception) as context:
            self.networker.change_backup_state('res_id', "4567", False)
        self.assertTrue('BACKUP016_CLIENT_INFORMATION_NOT_FOUND' in str(context.exception))

    @patch('backup.Networker.RestApiTemplate')
    def test_change_backup_state_to_FALSE(self, request_mock):
        instance = request_mock.return_value
        mock_response_put_positive = '<Response [204]>'
        instance.send_request.return_value = mock_response_put_positive
        self.networker = Networker("username", "password", "url")

        result = self.networker.change_backup_state(self.pause_input_data, "4567", False)
        self.assertEqual(result,mock_response_put_positive)

    @patch('backup.Networker.RestApiTemplate')
    def test_change_backup_state_to_TRUE(self, request_mock):
        instance = request_mock.return_value
        mock_response_put_positive = '<Response [204]>'
        instance.send_request.return_value = mock_response_put_positive
        self.networker = Networker("username", "password", "url")

        result = self.networker.change_backup_state(self.pause_input_data, "4567", True)
        self.assertEqual(result,mock_response_put_positive)

    def mock_clients(self):
        clients = {
        "clients": [
            {
                "aliases": [
                    "NVE-1",
                    "NVE-1.7",
                    "nve-1.7.xstest.local"
                ],
                "applicationInformation": [],
                "blockBasedBackup": False,
                "checkpointEnabled": False,
                "clientId": "15922ad4-00000004-5b582e6d-5b582e6c-00015000-91868456",
                "hostname": "nve-1.7.xstest.local",
                "indexBackupContent": False,
                "links": [
                    {
                        "href": "https://10.100.249.48:9090/nwrestapi/v2/global/clients/82.0.227.11.0.0.0.0.90.46.88.91.10.100.249.48",
                        "rel": "item"
                    }
                ],
                "nasDevice": False,
                "ndmp": False,
                "ndmpMultiStreamsEnabled": False,
                "ndmpVendorInformation": [],
                "parallelSaveStreamsPerSaveSet": False,
                "parallelism": 12,
                "protectionGroups": [],
                "remoteAccessUsers": [],
                "resourceId": {
                    "id": "82.0.227.11.0.0.0.0.90.46.88.91.10.100.249.48",
                    "sequence": 3
                },
                "saveSets": [
                    "All"
                ],
                "scheduledBackup": True,
                "tags": []
            },
            {
                "aliases": [
                    "NVE-1",
                    "NVE-1.7",
                    "nve-1.7.xstest.local"
                ],
                "applicationInformation": [],
                "backupCommand": "savepsm.sh",
                "blockBasedBackup": False,
                "checkpointEnabled": False,
                "clientId": "15922ad4-00000004-5b582e6d-5b582e6c-00015000-91868456",
                "hostname": "nve-1.7.xstest.local",
                "indexBackupContent": False,
                "links": [
                    {
                        "href": "https://10.100.249.48:9090/nwrestapi/v2/global/clients/45.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48",
                        "rel": "item"
                    }
                ],
                "nasDevice": False,
                "ndmp": False,
                "ndmpMultiStreamsEnabled": False,
                "ndmpVendorInformation": [],
                "parallelSaveStreamsPerSaveSet": False,
                "parallelism": 12,
                "protectionGroups": [
                    "NMC server"
                ],
                "remoteAccessUsers": [],
                "resourceId": {
                    "id": "45.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48",
                    "sequence": 3
                },
                "saveSets": [
                    "/nsr/nmc/nmcdb_stage"
                ],
                "scheduledBackup": True,
                "tags": []
            },
            {
                "aliases": [
                    "vc8",
                    "vc8.vslabs.vec.drhm01.fabshop.io"
                ],
                "applicationInformation": [],
                "backupType": "vProxy",
                "blockBasedBackup": False,
                "checkpointEnabled": False,
                "clientId": "c439a6b1-00000004-5b583be0-5b584f42-00025000-91868456",
                "hostname": "vc8.vslabs.vec.drhm01.fabshop.io",
                "indexBackupContent": False,
                "links": [
                    {
                        "href": "https://10.100.249.48:9090/nwrestapi/v2/global/clients/47.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48",
                        "rel": "item"
                    }
                ],
                "nasDevice": False,
                "ndmp": False,
                "ndmpMultiStreamsEnabled": False,
                "ndmpVendorInformation": [],
                "parallelSaveStreamsPerSaveSet": False,
                "parallelism": 4,
                "protectionGroups": [
                    "vcenter"
                ],
                "remoteAccessUsers": [],
                "resourceId": {
                    "id": "47.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48",
                    "sequence": 2
                },
                "saveSets": [
                    "All"
                ],
                "scheduledBackup": True,
                "tags": []
            }
        ],
        "count": 3
        }
        return clients

    def mock_pg(self):
        pg = {
            "comment": "Default protection group for workflow Bronze/Filesystem",
            "links": [
                {
                    "href": "https://10.100.249.48:9090/nwrestapi/v2/global/protectiongroups/Bronze-Filesystem",
                    "rel": "item"
                }
            ],
            "name": "Bronze-Filesystem",
            "resourceId": {
                "id": "152.0.227.11.0.0.0.0.90.46.88.91.10.100.249.48",
                "sequence": 17
            },
            "workItemQueries": [],
            "workItemSource": "Static",
            "workItemSubType": "None",
            "workItemType": "Client",
            "workItems": ["47.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48", "47.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48"]
        }
        return pg

    def mock_enable_success(self):
        response = \
            [
                {"step": 1,
                 "description": "Create the client",
                 "result": "Client already configured. Moving to the next step",
                 "error": {}
                },
                {"step": 2,
                 "description": "Add the client to the Protection Group",
                 "result": "Client added to the protection group.",
                 "error": {}
                }
            ]
        return response

    def mock_enable_new_client_success(self):
        response = \
            [
                {"step": 1,
                 "description": "Create the client",
                 "result": "Client created with Resource ID 8.2.250.6.0.0.0.0.76.63.163.91.10.100.249.48",
                 "error": {}
                 },
                {"step": 2,
                 "description": "Add the client to the Protection Group",
                 "result": "Client added to the protection group.",
                 "error": {}
                 }
            ]
        return response

    def mock_client(self):
        response = {"aliases": [
               "perftest2",
               "perftest2.xstest.local",
               "vra7",
               "vra7.3.1.xstest.local"
           ],
           "applicationInformation": [],
           "blockBasedBackup": False,
           "checkpointEnabled": False,
           "clientId": "c977c6b2-00000004-5ba8cd40-5bacc924-003c5000-91868456",
           "hostname": "perftest2.xstest.local",
           "indexBackupContent": False,
           "links": [
               {
                   "href": "https://10.100.249.48:9090/nwrestapi/v2/global/clients/8.2.250.6.0.0.0.0.76.63.163.91.10.100.249.48",
                   "rel": "item"
               }
           ],
           "nasDevice": False,
           "ndmp": False,
           "ndmpMultiStreamsEnabled": False,
           "ndmpVendorInformation": [],
           "parallelSaveStreamsPerSaveSet": False,
           "parallelism": 4,
           "protectionGroups": [
               "Bronze-Filesystem-Old"
           ],
           "remoteAccessUsers": [],
           "resourceId": {
               "id": "8.2.250.6.0.0.0.0.76.63.163.91.10.100.249.48",
               "sequence": 6
           },
           "saveSets": [
               "All"
           ],
           "scheduledBackup": True,
           "tags": []
       }
        return response

    def mock_error(self):
        response = {"error_code": "generic-request-error", "error_message": "error occurred"}
        return response

    def mock_enable_error(self):
        response = \
            [
                {"step": 1,
                 "description": "Create the client",
                 "result": "An error occurred",
                 "error": self.mock_error()
                 }
            ]
        return response

    def mock_jobs_reponse(self):
        jobs_response = {
                            "count": 1,
                            "jobs": [
                                {
                                    "adhocJob": False,
                                    "command": "savegrp -Z backup:traditional -v",
                                    "completionStatus": "Unknown",
                                    "dependentJobIds": [
                                        0
                                    ],
                                    "endTime": "2018-12-10T21:00:05-07:00",
                                    "exitCode": 0,
                                    "id": 162187,
                                    "itemIdLong": 162187,
                                    "links": [
                                        {
                                            "href": "https://10.100.249.48:9090/nwrestapi/v2/global/jobs/162187",
                                            "rel": "item"
                                        }
                                    ],
                                    "logFile": "/nsr/logs/policy/Bronze/Workflow1/backup_162187.raw",
                                    "message": "151761 1544500800 1 5 0 3565307712 21651 0 nve-1.7.xstest.local savegrp NSR notice 53 Action %s '%s' has initialized as '%s' with job id %u 4 0 18 backup traditional 0 6 backup 0 17 backup action job 5 6 162187\n129166 1544500800 2 5 0 3565307712 21651 0 nve-1.7.xstest.local savegrp NSR warning 30 No input workitems to process. 0\n148758 1544500805 1 5 0 3565307712 21651 0 nve-1.7.xstest.local savegrp NSR notice 71 Action %s '%s' with job id %u is exiting with status '%s', exit code %d 5 0 18 backup traditional 0 6 backup 5 6 162187 0 11 did not run 1 1 0\n",
                                    "name": "savegrp",
                                    "ndmp": False,
                                    "parentJobId": 162186,
                                    "previousJobId": 0,
                                    "rootParentJobId": 162186,
                                    "runOnHost": "nve-1.7.xstest.local",
                                    "siblingJobIds": [],
                                    "startTime": "2018-12-10T21:00:00-07:00",
                                    "state": "Completed",
                                    "stopped": True,
                                    "tenant": "",
                                    "type": "backup action job"
                                }]
                        }
        return jobs_response




