import log_forwarder.responseparser as responseparser
from log_forwarder.constants import LOG_FORWARDER_ERROR
from common.exceptions import TASException
import unittest


class TestResponseParser(unittest.TestCase):

    def test_parse_salt_script_response_is_success_for_windows(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_salt_script_response(self.mock_agent_positive_response['comment'],
                                                                 kernel_type='windows')
        expected_output = True
        self.assertEqual(actual_output, expected_output)

    def test_parse_salt_script_response_is_success_for_linux(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_salt_script_response(self.mock_agent_positive_response['comment'],
                                                                 kernel_type='linux')
        expected_output = True
        self.assertEqual(actual_output, expected_output)

    def test_parse_salt_script_response_handle_null_response(self):
        response_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE",
                           'err_message': LOG_FORWARDER_ERROR["LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE"],
                           'err_trace': {}}
        try:
            response_instance.parse_salt_script_response({}, kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_improper_response(self):
        response_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE",
                           'err_message': LOG_FORWARDER_ERROR["LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE"],
                           'err_trace': {}}
        try:
            response_instance.parse_salt_script_response(self.mock_response_incorrect, kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_script_execution_failed(self):
        response_instance = responseparser.ResponseParser()

        expected_output = {'err_code': 'LOG_FWRDR010_SALT_CONFIGURATION_ISSUE',
                           'err_trace': 'unable to apply states on VM. '
                                          'check salt-master configurations.',
                           'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR010_SALT_CONFIGURATION_ISSUE']}
        try:
            response_instance.parse_salt_script_response(self.mock_script_execution_failed,
                                                         kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_copy_agent_pkg_failed_windows(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'LOG_FWRDR002_PKG_COPY_FAILED_ERROR',
            'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR002_PKG_COPY_FAILED_ERROR'],
            'err_trace': 'File C:\\nimsoft-robot-x64.exe updated failed'}
        try:
            resp_instance.parse_salt_script_response(self.mock_copy_agent_rpm_failed_response,
                                                     kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_copy_agent_pkg_agent_failed_linux(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'LOG_FWRDR003_INSTALL_FAILED',
            'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR003_INSTALL_FAILED'],
            'err_trace': 'Source file salt://REPO/Nimsoft-install/nimldr/agent/nimldr-7.93.tar.Z not found'}
        try:
            resp_instance.parse_salt_script_response(self.mock_copy_agent_rpm_failed_response,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_install_agent_failed_windows(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'LOG_FWRDR003_INSTALL_FAILED',
            'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR003_INSTALL_FAILED']}
        try:
            resp_instance.parse_salt_script_response(self.mock_response_run_num_1,
                                                     kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_change_owner_failed(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'LOG_FWRDR004_CHANGE_OWNER_FAILED',
            'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR004_CHANGE_OWNER_FAILED']}
        try:
            resp_instance.parse_salt_script_response(self.mock_response_run_num_1,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_first_start_failed(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'LOG_FWRDR005_FIRST_START_FAILED',
            'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR005_FIRST_START_FAILED']}
        try:
            resp_instance.parse_salt_script_response(self.mock_response_run_num_2,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_deploy_server_failed(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'LOG_FWRDR006_DEPLOYMENT_SERVER_CONNECTION_FAILED',
            'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR006_DEPLOYMENT_SERVER_CONNECTION_FAILED']}
        try:
            resp_instance.parse_salt_script_response(self.mock_response_run_num_3,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_install_agent_failed_linux(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'LOG_FWRDR004_CHANGE_OWNER_FAILED',
            'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR004_CHANGE_OWNER_FAILED']}
        try:
            resp_instance.parse_salt_script_response(self.mock_response_run_num_4,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_service_start_failed(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'LOG_FWRDR007_SERVICE_START_ERROR',
            'err_message': LOG_FORWARDER_ERROR['LOG_FWRDR007_SERVICE_START_ERROR']}
        try:
            resp_instance.parse_salt_script_response(self.mock_response_run_num_5,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])

    def test_parse_salt_script_response_handle_runtime_exception(self):
        resp_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            resp_instance.parse_salt_script_response(None, kernel_type='linux')
            self.assertTrue('Unknown exception' in str(context.exception))

    def setUp(self):
        self.mock_agent_positive_response = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "start_time": "01:49:03.522591",
                              "result": True,
                              "duration": 28.615,
                              "__run_num__": 0,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "splunkuf_install_splunkuf"
                            },
                            "cmd_|-splunkuf_change_owner_before_firsttime_start|": {
                                  "comment": "Command '/bin/chown -R splunk.splunk /opt/splunkforwarder/bin/splunk'",
                                  "pchanges": {

                                  },
                                  "name": "splunkuf_change_owner_before_firsttime_start",
                                  "start_time": "01:49:03.551511",
                                  "result": True,
                                  "duration": 66.254,
                                  "__run_num__": 1,
                                  "changes": {
                                    "diff": "New file",
                                    "mode": "0644"
                                  },
                                  "__id__": "splunkuf_change_owner_before_firsttime_start"
                              },
                            'cmd_|-splunkuf_install_firsttime_start|-splunk start_|-run':
                                {'__run_num__': 2,
                                 'comment': 'Command "splunk start --accept-license --answer-yes --no-prompt --seed-passwd xStreamsplunk!" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': 'splunkuf_install_firsttime_start',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': '',
                                 '__id__': 'splunkuf_install_firsttime_start', 'result': True},

                            'cmd_|-splunkuf_deployserver_set|-splunkuf_deployserver_set_|-run':
                                {'__run_num__': 3,
                                 'comment': 'Command "splunk set deploy-poll" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': 'splunkuf_deployserver_set',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': '',
                                 '__id__': 'splunkuf_deployserver_set', 'result': True},
                            'cmd_|-splunkuf_change_owner_after_register|-splunk start_|-run':
                                {'__run_num__': 4,
                                 'comment': 'Command "chown -R splunk.splunk /splunk " run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': 'splunkuf_change_owner_after_register',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': '',
                                 '__id__': 'splunkuf_change_owner_after_register', 'result': True},
                            "cmd_|-splunkuf_restart_cmdrun|-rpm -Uvh /opt/nimsoft-robot.x86_64.rpm_|-run": {
                              "comment": "Command '/opt/splunkforwarder/bin/splunk restart' run",
                              "name": "splunkuf_restart_cmdrun",
                              "start_time": "01:49:03.618593",
                              "result": True,
                              "duration": 1090.287,
                              "__run_num__": 5,
                              "changes": {
                                "pid": 5191,
                                "retcode": 0,
                                "stderr": "",
                                "stdout": ""
                              },
                              "__id__": "splunkuf_restart_cmdrun"}}}]}}

        self.mock_copy_agent_rpm_failed_response = \
                    self.mock_agent_negative_response_status_false = \
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 0,
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}

        self.mock_response_run_num_1= \
                    self.mock_agent_negative_response_status_false = \
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 1,
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}

        self.mock_response_run_num_1= \
                    self.mock_agent_negative_response_status_false = \
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 1,
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}

        self.mock_response_run_num_2= \
                    self.mock_agent_negative_response_status_false = \
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              'comment': 'Command "splunk start --accept-license --answer-yes --no-prompt --seed-passwd xStreamsplunk!" run',
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 2,
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}

        self.mock_response_run_num_3= \
                    self.mock_agent_negative_response_status_false = \
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              'comment': 'Command "splunk start --accept-license --answer-yes --no-prompt --seed-passwd xStreamsplunk!" run',
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 3,
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}

        self.mock_response_run_num_4= \
                    self.mock_agent_negative_response_status_false = \
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 4,
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}

        self.mock_response_run_num_5= \
                    self.mock_agent_negative_response_status_false = \
                {'return':
                    [
                        {'test.local': {
                            "cmd_|/opt/splunkforwarder/bin/splunk restart|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_restart_cmdrun",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 5,
                              "__id__": "splunkuf_restart_cmdrun"
                            }}}]}

        self.mock_response_incorrect= \
                    self.mock_agent_negative_response_status_false = \
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "duration": 28.615,
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}

        self.mock_script_execution_failed = \
            {'return': [
                {'local': ["unable to execute script"]}
            ]}

