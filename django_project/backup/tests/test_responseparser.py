import backup.responseparser as responseparser
from common.exceptions import TASException
import unittest


class TestResponseParser(unittest.TestCase):

    def test_parse_networker_agent_install_script_response_success(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_install_success_response)
        expected_output = {'status': True, 'comment': ''}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_agent_windows_install_script_response_success(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_windows_success)
        expected_output = {'status': True, 'comment': ''}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_agent_install_script_response_handle_null_response(self):
        response_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            response_instance.parse_networker_agent_install_script_response(None)
            self.assertTrue('Response received after executing the state files '
                            'on the VM is not proper' in str(context.exception))

    def test_parse_networker_agent_install_script_response_handle_improper_response(self):
        response_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            response_instance.parse_networker_agent_install_script_response({'return': []})
            self.assertTrue('Response received after executing the state files '
                            'on the VM is not proper' in str(context.exception))

    def test_parse_networker_agent_install_script_response_handle_script_execution_failed(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response({'return':
                                                                      [{'backup_vm.xstest.local':
                                                                        ['unable to apply states on VM. '
                                                                         'check salt-master configurations.']}]})
        expected_output = {'status': False, 'comment': 'unable to apply states on VM. '
                                                       'check salt-master configurations.'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_agent_install_script_response_handle_linux_copy_on_minion_failed(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_rpm_copy_on_minion_failed)
        expected_output = {'status': False, 'comment': 'Process to copy networker agent '
                                                       'package on the VM failed due to : '
                                                       'File /opt/lgtoclnt.rpm not able to find'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_agent_install_script_response_handle_windows_copy_on_minion_failed(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_exe_copy_on_minion_failed)
        expected_output = {'status': False, 'comment': 'Process to copy networker agent '
                                                       'package on the VM failed due to : '
                                                       'File C:\\\\lgtoclnt-9.2.1.4.exe not found'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_agent_install_script_response_handle_agent_linux_install_on_minion_failed(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_rpm_install_on_minion_failed)
        expected_output = {'status': False, 'comment': 'Process to install networker agent '
                                                       'package on the VM failed due to : '
                                                       'specified rpm packages installation failed'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_agent_install_script_response_handle_agent_windows_install_on_minion_failed(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_exe_install_on_minion_failed)
        expected_output = {'status': False, 'comment': 'Process to install networker agent '
                                                       'package on the VM failed due to : '
                                                       'The named service nsrexecd is not available'}

    def test_parse_networker_agent_install_script_response_handle_linux_agent_service_start_failed(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_service_start_failed)
        expected_output = {'status': False, 'comment': 'Process to start the networker '
                                                       'service on the VM failed due to : '
                                                       'Command "/etc/init.d/networker start" failed'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_agent_install_script_response_handle_windows_agent_service_start_failed(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_windows_start_failed)
        expected_output = {'status': False, 'comment': 'Process to start the networker '
                                                       'service on the VM failed due to : '
                                                       'The named service nsrexecd did not start'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_agent_install_script_response_handle_windows_agent_autoenable_failed(self):
        response_instance = responseparser.ResponseParser()
        actual_output = response_instance.parse_networker_agent_install_script_response(self.mock_agent_windows_autostart_failed)
        expected_output = {'status': False, 'comment': 'Process to enable auto start in windows '
                                                       'service on the VM failed due to : '
                                                       'Command "sc config nsrexecd start=auto" failed'}
        self.assertEqual(actual_output, expected_output)


    ###################unit tests of parse_add_host_entry_script_response#############################
    def test_parse_add_host_entry_script_response_success(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_add_host_entry_script_response(self.mock_add_dns_entry_success)
        expected_output = {'status': True, 'comment': ''}
        self.assertEqual(actual_output, expected_output)

    def test_parse_add_host_entry_script_response_handle_adding_entry_failed(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_add_host_entry_script_response(self.mock_add_dns_entry_failed)
        expected_output = {'status': False, 'comment': 'Script failed to add host entry'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_add_host_entry_script_response_handle_script_execution_failure(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_add_host_entry_script_response(
            self.mock_add_dns_entry_script_execution_fail)
        expected_output = {'status': False, 'comment': 'unable to apply states on VM. '
                                                       'check salt-master configurations.'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_add_host_entry_script_response_handle_null_response_and_runtime_exception(self):
        resp_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            resp_instance.parse_add_host_entry_script_response({'return': []})
            self.assertTrue('Response received after executing the state files '
                            'on the VM is not proper' in str(context.exception))
            self.assertTrue('unknown exception ' in str(context.exception))

    ###################unit tests of parse_networker_response#############################
    def test_parse_networker_response_success(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_networker_response(self.mock_networker_parser_success_response,
                                                               'dummy')
        expected_output = {'target_vm': 'dummy', 'status': True, 'comment':
                           'Client added to the protection group.'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_response_handle_null_input(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_networker_response(None, 'dummy')
        expected_output = {'target_vm': 'dummy', 'status': False, 'comment':
                           'Unable to fulfill the request. Response is not '
                           'in proper format.', 'error_code': '500'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_response_handle_enable_backup_fail(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_networker_response(self.mock_networker_parser_enable_backup_fail,
                                                               'dummy')
        expected_output = {'target_vm': 'dummy', 'status': False, 'comment':
                           'error occurred', 'error_code': 'generic-request-error'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_response_handle_runtime_exception(self):
        resp_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            resp_instance.parse_networker_response(self.mock_networker_parser_enable_backup_fail,
                                                   'dummy')
            self.assertTrue('unknown exception ' in str(context.exception))

    def test_parse_minion_backup_cleanup_salt_response_success(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_minion_backup_cleanup_salt_response(self.mock_cleanup_all_pass, "vm")
        expected_output = {'target_vm': 'vm', 'status': True, 'comment':
                           'Cleanup successfully done'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_minion_backup_cleanup_salt_response_host_remove_fails(self):
        resp_instance = responseparser.ResponseParser()

        expected_output = {'err_code': 'BACKUP022_NW_DD_ENTRY_REMOVE_ERROR',
                           'err_message': 'Process to delete NW and DD entries on the VM failed due to : SALT HOST ERROR',
                           'err_trace': ""}
        try:
            resp_instance.parse_minion_backup_cleanup_salt_response(self.mock_cleanup_host_remove_fail, "vm")
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_minion_backup_cleanup_salt_response_uninstall_fails(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "BACKUP024_NW_UNINSTALL_ERROR",
                           'err_message': 'Process of uninstalling NW on VM failed due to : SALT UNINSTALL ERROR' ,
                           'err_trace': ""}
        try:
            resp_instance.parse_minion_backup_cleanup_salt_response(self.mock_cleanup_uninstall_fail, "vm")
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_minion_backup_cleanup_salt_response_file_remove_fails(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': 'BACKUP023_FILE_CLEANUP_ERROR',
                           'err_message': 'Process to delete NW Files on the VM failed due to : FILE REMOVE ERROR',
                           'err_trace': ""}
        try:
            resp_instance.parse_minion_backup_cleanup_salt_response(self.mock_cleanup_file_remove_fail, "vm")
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_minion_backup_cleanup_salt_response_incorrect_salt_response(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': 'BACKUP015_SALT_EXECUTION_ERROR',
                           'err_message': "Response received after executing the salt net api command is not proper ||"
                                          " Response received: {'status': False} ||"
                                          " Error Message: 'comment'",
                           'err_trace': ""}
        try:
            resp_instance.parse_minion_backup_cleanup_salt_response(self.mock_cleanup_incorrect_salt_response, "vm")
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_minion_backup_cleanup_salt_response_no_minions_found(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': 'BACKUP015_SALT_EXECUTION_ERROR',
                           'err_message': "Response received after executing the salt net api command is not proper ||"
                                          " Response received: {'comment': {'return': []}, 'status': True} || "
                                          "Error Message: list index out of range",
                           'err_trace': ""}
        try:
            resp_instance.parse_minion_backup_cleanup_salt_response(self.mock_cleanup_no_minions_found, "vm")
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_minion_backup_cleanup_salt_response_runtime_exception(self):
        resp_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            resp_instance.parse_minion_backup_cleanup_salt_response(self.mock_cleanup_host_remove_fail, 'vm')
            self.assertTrue('unknown exception ' in str(context.exception))

    def test_parse_networker_minion_host_comment_salt_response_success(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_networker_minion_host_comment_salt_response(self.mock_comment_all_pass, "vm")
        expected_output = {'target_vm': 'vm', 'status': True, 'comment':
                           'Minion Entry Successfully commented'}
        self.assertEqual(actual_output, expected_output)

    def test_parse_networker_minion_host_comment_salt_response_host_comment_fails(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "BACKUP025_NW_DD_ENTRY_REMOVE_ERROR",
                           'err_message': "Process to commenting Minion host entry on "
                                          "the networker failed due to : SALT HOST ERROR",
                           'err_trace': ""}
        try:
            resp_instance.parse_networker_minion_host_comment_salt_response(self.mock_comment_host_fail, "vm")
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_networker_minion_host_comment_salt_response_incorrect_salt_response(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': 'BACKUP015_SALT_EXECUTION_ERROR',
                           'err_message': "Response received after executing the salt net api command is not proper ||"
                                          " Response received: {'status': False} || Error Message: 'comment'",
                           'err_trace': ""}
        try:
            resp_instance.parse_networker_minion_host_comment_salt_response(self.mock_comment_incorrect_salt_response, "vm")
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_networker_minion_host_comment_salt_response_no_minions_found(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': 'BACKUP015_SALT_EXECUTION_ERROR',
                           'err_message': "Response received after executing the salt net api command is not proper "
                                          "|| Response received: {'comment': {'return': []}, 'status': True} "
                                          "|| Error Message: list index out of range",
                           'err_trace': ""}
        try:
            resp_instance.parse_networker_minion_host_comment_salt_response(self.mock_comment_no_minions_found, "vm")
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_networker_minion_host_comment_salt_response_runtime_exception(self):
        resp_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            resp_instance.parse_networker_minion_host_comment_salt_response(self.mock_comment_host_fail, 'vm')
            self.assertTrue('unknown exception ' in str(context.exception))

    def setUp(self):
        self.mock_cleanup_all_pass = {'status': True, 'comment': {'return':[{'minion': {'1':{'__run_num__': 0, 'result': True},
                                                                                        '2':{'__run_num__': 1, 'result': True},
                                                                                        '3':{'__run_num__': 2, 'result': True},
                                                                                        '4':{'__run_num__': 3, 'result': True},
                                                                                        '5':{'__run_num__': 4, 'result': True},
                                                                                        '6':{'__run_num__': 5, 'result': True},
                                                                                        '7':{'__run_num__': 6, 'result': True}}}]}}

        self.mock_cleanup_host_remove_fail = {'status': True, 'comment': {'return':[{'minion': {'1':{'__run_num__': 0, 'result': True},
                                                                                                '2':{'__run_num__': 1, 'result': True},
                                                                                                '3':{'__run_num__': 2, 'result': True},
                                                                                                '4':{'__run_num__': 3, 'result': True},
                                                                                                '5':{'__run_num__': 4, 'result': False, 'comment': 'SALT HOST ERROR'},
                                                                                                '6':{'__run_num__': 5, 'result': True},
                                                                                                '7':{'__run_num__': 6, 'result': True}}}]}}

        self.mock_cleanup_uninstall_fail  = {'status': True, 'comment': {'return':[{'minion':  {'1':{'__run_num__': 0, 'result': True},
                                                                                                '2':{'__run_num__': 1, 'result': True},
                                                                                                '3':{'__run_num__': 2, 'result': True},
                                                                                                '4':{'__run_num__': 3, 'result': True},
                                                                                                '5':{'__run_num__': 4, 'result': True},
                                                                                                '6':{'__run_num__': 5, 'result': False, 'comment': 'SALT UNINSTALL ERROR'},
                                                                                                '7':{'__run_num__': 6, 'result': True}}}]}}

        self.mock_cleanup_file_remove_fail = {'status': True, 'comment': {'return':[{'minion': {'1':{'__run_num__': 0, 'result': True},
                                                                                                '2':{'__run_num__': 1, 'result': True},
                                                                                                '3':{'__run_num__': 2, 'result': True},
                                                                                                '4':{'__run_num__': 3, 'result': True},
                                                                                                '5':{'__run_num__': 4, 'result': True},
                                                                                                '6':{'__run_num__': 5, 'result': True},
                                                                                                '7':{'__run_num__': 6, 'result': False, 'comment': 'FILE REMOVE ERROR'}}}]}}

        self.mock_cleanup_incorrect_salt_response = {'status': False}
        self.mock_cleanup_no_minions_found = {'status': True, 'comment': {'return':[]}}

        self.mock_comment_all_pass = {'status': True, 'comment': {'return':[{'minion': {'1':{'__run_num__': 0, 'result': True}}}]}}
        self.mock_comment_host_fail = {'status': True, 'comment': {'return':[{'minion': {'1':{'__run_num__': 0, 'result': False, 'comment': 'SALT HOST ERROR'}}}]}}
        self.mock_comment_incorrect_salt_response = {'status': False}
        self.mock_comment_no_minions_found = {'status': True, 'comment': {'return': []}}

        self.mock_agent_install_success_response = \
            {'return':
             [
                 {'backup_vm.xstest.local': {
                     'file_|-/opt/lgtoclnt.rpm_|-managed': {
                         '__sls__': 'networker/unix_client', '__run_num__': 0,
                         'comment': 'File /opt/lgtoclnt.rpm is in the correct state',
                         'start_time': '04:35:10.057890', 'duration': 859.522,
                         'name': '/opt/lgtoclnt.rpm', 'changes': {}, 'pchanges': {},
                         '__id__': '/opt/lgtoclnt-1.x86_64.rpm', 'result': True},
                     'cmd_|-start_networker_|-/etc/init.d/networker start1_|-run':
                         {'__run_num__': 2,
                          'comment': 'Command "/etc/init.d/networker start" run',
                          'start_time': '04:35:11.914480', 'duration': 7.474,
                          'name': '/etc/init.d/networker start',
                          'changes': {'pid': 18283, 'retcode': 0,
                                      'stderr': '', 'stdout': ''},
                          '__sls__': 'networker/unix_client',
                          '__id__': 'start_networker', 'result': True},
                     'pkg_|-install_lgtoclnt.rpm_|-installed': {
                         '__run_num__': 1, 'comment': 'All specified packages are already installed',
                         'start_time': '04:35:11.528557', 'duration': 384.186,
                         'name': 'install_lgtoclnt.rpm', 'changes': {},
                         '__sls__': 'networker/unix_client',
                         '__id__': 'install_lgtoclnt.rpm', 'result': True}}}]}

        self.mock_agent_windows_success = \
            {'return': [{'windows-latest.496D2042426EB955A741B5B3C9C80C34':
                             {'cmd_|-install_lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0_|-run':
                                  {'comment': 'Command "C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0" run',
                                   'name': 'C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0',
                                   'start_time': '13:36:49.470000', 'result': True, 'duration': 14294.0,
                                   '__run_num__': 1, '__sls__': 'networker.win_client',
                                   'changes': {'pid': 2804, 'retcode': 0, 'stderr': '', 'stdout': ''},
                                   '__id__': 'install_lgtoclnt-9.2.1.4.exe'}, 'service_|-nsrexecd_|-nsrexecd_|-running':
                                  {'comment': 'The service nsrexecd is already running', 'name': 'nsrexecd',
                                  'start_time': '13:37:03.764000', 'result': True, 'duration': 16.0,
                                  '__run_num__': 2, '__sls__': 'networker.win_client', 'changes': {}, '__id__': 'nsrexecd'},
                                  'cmd_|-remove_delay_start_|-sc config nsrexecd start=auto_|-run':
                                  {'comment': 'Command "sc config nsrexecd start=auto" run', 'name': 'sc config nsrexecd start=auto',
                                  'start_time': '13:37:03.780000', 'result': True, 'duration': 15.0,
                                  '__run_num__': 3, '__sls__': 'networker.win_client',
                                  'changes': {'pid': 880, 'retcode': 0, 'stderr': '', 'stdout': '[SC] ChangeServiceConfig SUCCESS'},
                                  '__id__': 'remove_delay_start'}, 'file_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-managed':
                                  {'comment': 'File C:\\\\lgtoclnt-9.2.1.4.exe updated', 'pchanges': {}, 'name': 'C:\\\\lgtoclnt-9.2.1.4.exe',
                                   'start_time': '13:36:47.525000', 'result': True, 'duration': 1945.0,
                                   '__run_num__': 0, '__sls__': 'networker.win_client', 'changes': {'diff': 'New file'},'__id__': 'C:\\\\lgtoclnt-9.2.1.4.exe'}}}]}

        self.mock_agent_rpm_copy_on_minion_failed = \
            {'return':
                [
                    {'backup_vm.xstest.local': {
                        'file_|-/opt/lgtoclnt.rpm_|-managed': {
                            '__sls__': 'networker/unix_client', '__run_num__': 0,
                            'comment': 'File /opt/lgtoclnt.rpm not able to find',
                            'start_time': '04:35:10.057890', 'duration': 859.522,
                            'name': '/opt/lgtoclnt.rpm', 'changes': {}, 'pchanges': {},
                            '__id__': '/opt/lgtoclnt-1.x86_64.rpm', 'result': False}
                    }}]}

        self.mock_agent_exe_copy_on_minion_failed = \
            {'return': [{'windows-latest.496D2042426EB955A741B5B3C9C80C34': {
                             'file_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-managed':{
                                  'comment': 'File C:\\\\lgtoclnt-9.2.1.4.exe not found', 'pchanges': {},
                                  'name': 'C:\\\\lgtoclnt-9.2.1.4.exe',
                                  'start_time': '13:36:47.525000', 'result': False, 'duration': 1945.0,
                                  '__run_num__': 0, '__sls__': 'networker.win_client',
                                  'changes': {'diff': 'New file'}, '__id__': 'C:\\\\lgtoclnt-9.2.1.4.exe'}}}]}

        self.mock_agent_rpm_install_on_minion_failed = \
            {'return':
                [
                    {'backup_vm.xstest.local': {
                        'file_|-/opt/lgtoclnt.rpm_|-managed': {
                            '__sls__': 'networker/unix_client', '__run_num__': 0,
                            'comment': 'File /opt/lgtoclnt.rpm is in the correct state',
                            'start_time': '04:35:10.057890', 'duration': 859.522,
                            'name': '/opt/lgtoclnt.rpm', 'changes': {}, 'pchanges': {},
                            '__id__': '/opt/lgtoclnt-1.x86_64.rpm', 'result': True},
                        'pkg_|-install_lgtoclnt.rpm_|-installed': {
                            '__run_num__': 1, 'comment': 'specified rpm packages installation failed',
                            'start_time': '04:35:11.528557', 'duration': 384.186,
                            'name': 'install_lgtoclnt.rpm', 'changes': {},
                            '__sls__': 'networker/unix_client',
                            '__id__': 'install_lgtoclnt.rpm', 'result': False}}}]}

        self.mock_agent_exe_install_on_minion_failed = \
            {
                'return': [{
                    'testwindows.C4E12042CA71FBC3423240CDE06F1DAB': {
                        'cmd_|-install_lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0_|-run': {
                            'comment': 'Command "C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0" run',
                            'name': 'C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0',
                            'start_time': '14:48:14.735000',
                            'result': True,
                            'duration': 14040.0,
                            '__run_num__': 1,
                            '__sls__': 'networker.win_client',
                            'changes': {
                                'pid': 1300,
                                'retcode': 0,
                                'stderr': '',
                                'stdout': ''
                            },
                            '__id__': 'install_lgtoclnt-9.2.1.4.exe'
                        },
                        'service_|-nsrexecd_|-nsrexecd_|-running': {
                            'comment': 'The named service nsrexecd is not available',
                            'name': 'nsrexecd',
                            'start_time': '14:48:28.775000',
                            'result': False,
                            'duration': 0.0,
                            '__run_num__': 2,
                            '__sls__': 'networker.win_client',
                            'changes': {},
                            '__id__': 'nsrexecd'
                        },
                        'cmd_|-remove_delay_start_|-sc config nsrexecd start=auto_|-run': {
                            'comment': 'Command "sc config nsrexecd start=auto" run',
                            'name': 'sc config nsrexecd start=auto',
                            'start_time': '14:48:28.775000',
                            'result': False,
                            'duration': 16.0,
                            '__run_num__': 3,
                            '__sls__': 'networker.win_client',
                            'changes': {
                                'pid': 1388,
                                'retcode': 1639,
                                'stderr': '',
                                'stdout': 'DESCRIPTION:\r\n        Modifies a service entry in the registry and Service Database.\r\nUSAGE:\r\n        '
                                          'sc <server> config [service name] <option1> <option2>...\r\n\r\nOPTIONS:\r\nNOTE: The option name includes the equal sign.\r\n      '
                                          'A space is required between the equal sign and the value.\r\n type= <own|share|interact|kernel|filesys|rec|adapt>\r\n '
                                          'start= <boot|system|auto|demand|disabled|delayed-auto>\r\n error= <normal|severe|critical|ignore>\r\n binPath= <BinaryPathName>\r\n '
                                          'group= <LoadOrderGroup>\r\n tag= <yes|no>\r\n depend= <Dependencies(separated by / '
                                          '(forward slash))>\r\n obj= <AccountName|ObjectName>\r\n DisplayName= <display name>\r\n password= <password>'
                            },
                            '__id__': 'remove_delay_start'
                        },
                        'file_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-managed': {
                            'comment': 'File C:\\\\lgtoclnt-9.2.1.4.exe updated',
                            'pchanges': {},
                            'name': 'C:\\\\lgtoclnt-9.2.1.4.exe',
                            'start_time': '14:48:12.551000',
                            'result': True,
                            'duration': 2184.0,
                            '__run_num__': 0,
                            '__sls__': 'networker.win_client',
                            'changes': {
                                'diff': 'New file'
                            },
                            '__id__': 'C:\\\\lgtoclnt-9.2.1.4.exe'
                        }
                    }
                }]
            }


        self.mock_agent_service_start_failed = \
            {'return':
             [
                 {'backup_vm.xstest.local': {
                     'file_|-/opt/lgtoclnt.rpm_|-managed': {
                         '__sls__': 'networker/unix_client', '__run_num__': 0,
                         'comment': 'File /opt/lgtoclnt.rpm is in the correct state',
                         'start_time': '04:35:10.057890', 'duration': 859.522,
                         'name': '/opt/lgtoclnt.rpm', 'changes': {}, 'pchanges': {},
                         '__id__': '/opt/lgtoclnt-1.x86_64.rpm', 'result': True},
                     'cmd_|-start_networker_|-/etc/init.d/networker start1_|-run':
                         {'__run_num__': 2,
                          'comment': 'Command "/etc/init.d/networker start" failed',
                          'start_time': '04:35:11.914480', 'duration': 7.474,
                          'name': '/etc/init.d/networker start',
                          'changes': {'pid': 18283, 'retcode': 0,
                                      'stderr': '', 'stdout': ''},
                          '__sls__': 'networker/unix_client',
                          '__id__': 'start_networker', 'result': False},
                     'pkg_|-install_lgtoclnt.rpm_|-installed': {
                         '__run_num__': 1, 'comment': 'All specified packages are already installed',
                         'start_time': '04:35:11.528557', 'duration': 384.186,
                         'name': 'install_lgtoclnt.rpm', 'changes': {},
                         '__sls__': 'networker/unix_client',
                         '__id__': 'install_lgtoclnt.rpm', 'result': True}}}]}

        self.mock_agent_windows_start_failed = \
            {
                'return': [{
                    'testwindows.C4E12042CA71FBC3423240CDE06F1DAB': {
                        'cmd_|-install_lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0_|-run': {
                            'comment': 'Command "C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0" run',
                            'name': 'C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0',
                            'start_time': '14:48:14.735000',
                            'result': True,
                            'duration': 14040.0,
                            '__run_num__': 1,
                            '__sls__': 'networker.win_client',
                            'changes': {
                                'pid': 1300,
                                'retcode': 0,
                                'stderr': '',
                                'stdout': ''
                            },
                            '__id__': 'install_lgtoclnt-9.2.1.4.exe'
                        },
                        'service_|-nsrexecd_|-nsrexecd_|-running': {
                            'comment': 'The named service nsrexecd did not start',
                            'name': 'nsrexecd',
                            'start_time': '14:48:28.775000',
                            'result': False,
                            'duration': 0.0,
                            '__run_num__': 2,
                            '__sls__': 'networker.win_client',
                            'changes': {},
                            '__id__': 'nsrexecd'
                        },
                        'cmd_|-remove_delay_start_|-sc config nsrexecd start=auto_|-run': {
                            'comment': 'Command "sc config nsrexecd start=auto" run',
                            'name': 'sc config nsrexecd start=auto',
                            'start_time': '14:48:28.775000',
                            'result': False,
                            'duration': 16.0,
                            '__run_num__': 3,
                            '__sls__': 'networker.win_client',
                            'changes': {
                                'pid': 1388,
                                'retcode': 1639,
                                'stderr': '',
                                'stdout': 'DESCRIPTION:\r\n        Modifies a service entry in the registry and Service Database.\r\nUSAGE:\r\n        '
                                          'sc <server> config [service name] <option1> <option2>...\r\n\r\nOPTIONS:\r\nNOTE: The option name includes the equal sign.\r\n      '
                                          'A space is required between the equal sign and the value.\r\n type= <own|share|interact|kernel|filesys|rec|adapt>\r\n '
                                          'start= <boot|system|auto|demand|disabled|delayed-auto>\r\n error= <normal|severe|critical|ignore>\r\n binPath= <BinaryPathName>\r\n '
                                          'group= <LoadOrderGroup>\r\n tag= <yes|no>\r\n depend= <Dependencies(separated by / '
                                          '(forward slash))>\r\n obj= <AccountName|ObjectName>\r\n DisplayName= <display name>\r\n password= <password>'
                            },
                            '__id__': 'remove_delay_start'
                        },
                        'file_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-managed': {
                            'comment': 'File C:\\\\lgtoclnt-9.2.1.4.exe updated',
                            'pchanges': {},
                            'name': 'C:\\\\lgtoclnt-9.2.1.4.exe',
                            'start_time': '14:48:12.551000',
                            'result': True,
                            'duration': 2184.0,
                            '__run_num__': 0,
                            '__sls__': 'networker.win_client',
                            'changes': {
                                'diff': 'New file'
                            },
                            '__id__': 'C:\\\\lgtoclnt-9.2.1.4.exe'
                        }
                    }
                }]
            }

        self.mock_add_dns_entry_success = \
            {'return':
                 [{'rhel74':
                       {'host_|-10.100.249.46_|-10.100.249.46_|-only':
                            {'__run_num__': 0, 'start_time': '03:57:06.644591',
                             'comment': 'successfully changed 10.100.249.46 from "" to "DDVE.xstest.local DDVE"',
                             'name': '10.100.249.46', 'result': True,
                             'changes': {'10.100.249.46': {'old': '', 'new': 'DDVE.xstest.local DDVE'}},
                             'duration': 1.104, '__sls__': 'networker/etchosts', '__id__': '10.100.249.46'},
                        'host_|-10.100.249.48_|-10.100.249.48_|-only':
                            {'__run_num__': 1, 'start_time': '03:57:06.645807',
                             'comment': 'successfully changed 10.100.249.48 from "" to "NVE-1.7.xstest.local NVE-1.7"',
                             'name': '10.100.249.48', 'result': True,
                             'changes': {'10.100.249.48': {'old': '', 'new': 'NVE-1.7.xstest.local NVE-1.7'}},
                             'duration': 0.877, '__sls__': 'networker/etchosts', '__id__': '10.100.249.48'}}}]}

        self.mock_add_dns_entry_failed = \
            {'return':
                [{'rhel74':
                  {'host_|-10.100.249.46_|-10.100.249.46_|-only':
                       {'__run_num__': 0, 'start_time': '03:57:06.644591',
                        'comment': 'failed in changing 10.100.249.46 from "" to "DDVE.xstest.local DDVE"',
                        'name': '10.100.249.46', 'result': False,
                        'changes': {'10.100.249.46': {'old': '', 'new': 'DDVE.xstest.local DDVE'}},
                        'duration': 1.104, '__sls__': 'networker/etchosts', '__id__': '10.100.249.46'},
                   }}]}

        self.mock_add_dns_entry_script_execution_fail = \
            {'return':
                [
                    {'backup_vm.xstest.local': ["unable to execute script"]}]}

        self.mock_networker_parser_success_response = \
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

        self.mock_networker_parser_adding_client_fail = \
            [
                {'step': 1, 'description': 'Create the client',
                 'error': {}, 'result': 'Client created with Resource ID '
                                        '83.0.243'
                 },
                {"step": 2,
                 "description": "Add the client to the Protection Group",
                 "result": "An error occurred",
                 "error": {"error_message": "error occured while adding client to protection group",
                           "error_code": 500}
                 }
            ]

        self.mock_networker_parser_enable_backup_fail = \
            [
                {"step": 1,
                 "description": "Create the client",
                 "result": "An error occurred",
                 "error": {"error_code": "generic-request-error", "error_message": "error occurred"}
                 }
            ]

        self.mock_agent_windows_autostart_failed = \
            {'return': [{'windows-latest.496D2042426EB955A741B5B3C9C80C34':
                             {
                                 'cmd_|-install_lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0_|-run':
                                     {
                                         'comment': 'Command "C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0" run',
                                         'name': 'C:\\\\lgtoclnt-9.2.1.4.exe /s /q InstallLevel=100 ConfigureFirewall=0',
                                         'start_time': '13:36:49.470000', 'result': True, 'duration': 14294.0,
                                         '__run_num__': 1, '__sls__': 'networker.win_client',
                                         'changes': {'pid': 2804, 'retcode': 0, 'stderr': '', 'stdout': ''},
                                         '__id__': 'install_lgtoclnt-9.2.1.4.exe'},
                                 'service_|-nsrexecd_|-nsrexecd_|-running':
                                     {'comment': 'The service nsrexecd is already running', 'name': 'nsrexecd',
                                      'start_time': '13:37:03.764000', 'result': True, 'duration': 16.0,
                                      '__run_num__': 2, '__sls__': 'networker.win_client', 'changes': {},
                                      '__id__': 'nsrexecd'},
                                 'cmd_|-remove_delay_start_|-sc config nsrexecd start=auto_|-run':
                                     {'comment': 'Command "sc config nsrexecd start=auto" failed',
                                      'name': 'sc config nsrexecd start=auto',
                                      'start_time': '13:37:03.780000', 'result': False, 'duration': 15.0,
                                      '__run_num__': 3, '__sls__': 'networker.win_client',
                                      'changes': {'pid': 880, 'retcode': 0, 'stderr': '',
                                                  'stdout': '[SC] ChangeServiceConfig SUCCESS'},
                                      '__id__': 'remove_delay_start'},
                                 'file_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-C:\\\\lgtoclnt-9.2.1.4.exe_|-managed':
                                     {'comment': 'File C:\\\\lgtoclnt-9.2.1.4.exe updated', 'pchanges': {},
                                      'name': 'C:\\\\lgtoclnt-9.2.1.4.exe',
                                      'start_time': '13:36:47.525000', 'result': True, 'duration': 1945.0,
                                      '__run_num__': 0, '__sls__': 'networker.win_client',
                                      'changes': {'diff': 'New file'}, '__id__': 'C:\\\\lgtoclnt-9.2.1.4.exe'}}}]}