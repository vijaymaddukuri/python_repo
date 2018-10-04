# ------------------------------------------------------------------------------
# Copyright (C) 2016-2017 DELL EMC Corporation. All Rights Reserved.

# This software contains the intellectual property of DELL EMC Corporation
# or is licensed to DELL EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of DELL  EMC.

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import requests
import pydevd
import redis
import copy
import jmespath
import time

from ansible.plugins.callback import CallbackBase
# import OzoneAPI
# from ansible.module_utils.urls import open_url
from ansible.plugins.callback.default import CallbackModule as CallbackModule_default
from ansible import constants as C

RETRY_ERRORS = [ "SMIS", "channel is not opened", "Connection aborted", "Connection refused", "Remote end closed connection without response" ]

OZONE_ANSIBLE_API = 'api/ansible/'
# Set these env variables before running ansible playbook
# export ANSIBLE_CALLBACK_PLUGINS=callback_plugins
# export ANSIBLE_STDOUT_CALLBACK=ozone
# export KUE_HOSTNAME='127.0.0.1'
# export KUE_PORT='9000'
# export OZONE_HOSTNAME='127.0.0.1'
# export OZONE_PORT='9000'
# export OZONE_USERNAME='ansibleozoneconnect@ozone.com'
# export OZONE_PASSWORD='ansibleConnect'
# export OZONE_ANSIBLE_ID='57fe90dc87344f5c36790fae'

MAX_CONNECTION_RETRIES = 10


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'ozone'

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)

        self.defaultCallback = CallbackModule_default()
        # self.defaultCallback.__init__(display)

        self.results = []
        self.stats = None
        self.killFlag = False

        self.kue_host = os.getenv('KUE_HOSTNAME')
        self.kue_port = os.getenv('KUE_PORT')
        self.ozone_host = os.getenv('OZONE_HOSTNAME')
        self.ozone_port = os.getenv('OZONE_PORT')
        self.ozone_username = os.getenv('OZONE_USERNAME')
        self.ozone_password = os.getenv('OZONE_PASSWORD')
        self.ozone_redis_password = os.getenv('OZONE_REDIS_PASSWORD')
        self.ozone_ansible_id = os.getenv('OZONE_ANSIBLE_ID')

        self.ozone_redis_host = "localhost"
        self.ozone_redis_port = 6379
        self.ozone_redis_password = self.ozone_redis_password
        self.access_token = None

        self.subscribe_to_kill()
        # try:
        #     self.login()
        #     print("Logged in " + self.access_token)
        # except Exception as loginException:
        #     print("Log in Error " + str(loginException))

    def format_url(self, api):
        api = api.replace("http://{0}:{1}/".format(self.kue_host, self.kue_port), "")
        return "http://{0}:{1}/{2}".format(self.kue_host, self.kue_port, api.strip("/"))

    # Submit HTTP Request
    def get_headers(self, content_type='application/json', xml=False, access_token=None):
        if xml:
            headers = {'Content-Type': content_type, 'ACCEPT': 'application/xml, application/octet-stream'}
        else:
            headers = {'Content-Type': content_type, 'ACCEPT': 'application/json, application/octet-stream'}

        if access_token:
            headers['authorization'] = 'Bearer ' + access_token
        elif self.access_token:
            headers['authorization'] = 'Bearer ' + self.access_token

        return headers

    # Submit HTTP Request
    def submit_http_request(self, http_method, uri, content_type='application/json', payload=None, xml=False,
                            trylogin=True,
                            files=None, access_token=None):
        retry = True
        retries = 0
        while retry:
            retries += 1
            if MAX_CONNECTION_RETRIES < retries:
                raise Exception("Unable to connect to OzoneAPI. Max retries exceeded.")
            retry = False
            try:
                return self.__submit_http_request(http_method, uri, content_type, payload, xml, trylogin, files,
                                                  access_token)
            except Exception as e:
                # logger.warning("An error occurred while sending a request to vRealize Orchestrator. %s" % str(e))
                for RETRY_ERROR in RETRY_ERRORS:
                    if RETRY_ERROR in str(e):
                        retry = True
                        break
                if retry is False:
                    raise e

    def __submit_http_request(self, http_method, uri, content_type='application/json', payload=None, xml=False,
                              trylogin=True,
                              files=None, access_token=None):
        headers = self.get_headers(content_type, xml, access_token)

        url = self.format_url(uri)
        # vro_auth = requests.auth.HTTPBasicAuth(admin_user, admin_password)
        session = requests.session()

        if http_method == 'GET':
            response = session.get(url, verify=False, headers=headers)
        elif http_method == 'POST':
            response = session.post(url, data=payload, verify=False, headers=headers, files=files)
        elif http_method == 'PUT':
            response = session.put(url, data=payload, headers=headers, verify=False)
        else:
            raise Exception("Unknown/Unsupported HTTP method: " + http_method)

        if response.status_code and response.status_code == requests.codes['ok'] or response.status_code == 202:
            # _logger.debug("Response: %s" % response.text)
            return response
        else:
            if response.status_code == 401:
                # Try re login only once.
                if trylogin:
                    # _logger.debug("Got an 401 error, trying to re-login")
                    self.login()
                    return self.submit_http_request(http_method, uri, content_type, payload, xml, False)
                else:
                    # 401 response is html, so not parsing response
                    raise Exception(401, "Unauthorized")
            try:
                error_json = json.loads(response.text)
                raise Exception("%s: %s" % (str(response.status_code), error_json["details"]))
            except Exception as error_parsing_exception:
                raise Exception("%s: %s" % (str(response.status_code), response.text))

    def login(self):
        response = self.submit_http_request('POST', 'auth/local',
                                            payload=json.dumps(
                                                {'email': self.ozone_username, 'password': self.ozone_password}),
                                            trylogin=False)
        response_json = json.loads(response.text)
        self.access_token = response_json['token']

    def message_handler(self, message):
        print("Received Job Kill Message. Checking if it is for current job - %s" % message)
        try:
            messageDataJson = json.loads(message['data'], "utf-8")
            if isinstance(messageDataJson, dict) and 'ansibleId' in messageDataJson and messageDataJson['ansibleId'] == self.ozone_ansible_id:
                print("Marking job to Kill")
                os.environ["OZONE_KILL_FLAG"] = "KILL_JOB"
                if self.kill_thread:
                    self.kill_thread.stop()
        except Exception as ex:
            print("Error processing kill message %s" % ex)

    def subscribe_to_kill(self):

        # Connect to redis server on the Ozone server
        REDIS = redis.StrictRedis(host=self.ozone_redis_host, port=self.ozone_redis_port, password=self.ozone_redis_password)
        REDIS_PUBSUB = REDIS.pubsub()

        # Subscribe to 'python:run' messaging service
        REDIS_PUBSUB.subscribe(**{'kue:stop': self.message_handler})

        self.kill_thread = REDIS_PUBSUB.run_in_thread(sleep_time=0.001)

    def get_ozone_ansible_object(self, ozone_ansible_object_id):
        response = self.submit_http_request('GET', OZONE_ANSIBLE_API + ozone_ansible_object_id)
        response_json = json.loads(response.text)
        return response_json

    def update_ozone_ansible_object(self, ansibleState):

        ozone_ansible_object_update = {
            'ansibleState': ansibleState,
            'ansibleResults': self.results
        }

        if self.stats:
            ozone_ansible_object_update['ansibleStats'] = self.stats

        payload = {
           "type": "statusUpdate",
           "data": {
             "ozone_host": self.ozone_host,
             "ozone_port": self.ozone_port,
             "ozone_username": self.ozone_username,
             "ozone_password": self.ozone_password,
             "ozone_ansible_id": self.ozone_ansible_id,
                 "ansibleObjectUpdate": ozone_ansible_object_update
               },
           "options": {
             "attempts": 10
           }
        }

        try:
            response = self.submit_http_request('POST', 'job',
                                           payload=json.dumps(payload))
        except Exception as updateException:
            print("UpdateException - %s" % updateException)

    def _new_play(self, playObject):
        return {
            'play': {
                'name': playObject.name,
                'id': str(playObject._uuid)
            },
            'tasks': [],
            'start_time': int(time.time()) * 1000
        }

    def _new_task(self, task, host=None):
        # if self.killFlag:

        return {
            'task': {
                'name': task.name,
                'id': str(task._uuid)
            },
            'hosts': host or {},
            'status': 'running'
        }

    def custom_print(self, content):
        print('--------BEGIN--------')
        # print(content)
        print(json.dumps(content, indent=4, sort_keys=True))
        print('--------END--------')

    def cleanData(self, jsonData):
        """
        Strip unwanted/sensitive data from results
        :param jsonData:
        :return:
        """
        unnecessary_keys = ['invocation', 'ansible_facts']
        if isinstance(jsonData, dict):
            for (key, value) in jsonData.iteritems():

                if key in unnecessary_keys:
                    jsonData[key] = 'CONTENT REMOVED'
                else:
                    self.cleanData(jsonData[key])

        elif isinstance(jsonData, list):
            for item in jsonData:
                self.cleanData(item)

        return jsonData

    def replaceDotInKey(self, jsonData):
        """
        MongoDB doesnt like "." or "$" in key. This function replaces all such occurrences with _dot_ or _dollar_
        :param jsonData:
        :return:
        """
        if isinstance(jsonData, dict):
            for (key, value) in jsonData.iteritems():

                newkey = self.replaceDotInKey(key)

                if key != newkey:
                    jsonData[newkey] = jsonData[key]
                    del jsonData[key]
                    key = newkey

                self.replaceDotInKey(jsonData[key])

        elif isinstance(jsonData, list):
            for item in jsonData:
                self.replaceDotInKey(item)
        elif isinstance(jsonData, unicode) or isinstance(jsonData, str):
            return jsonData and jsonData.replace(".", "_dot_").replace("$", "_dollar_")

        return jsonData

    def get_result_play_by_id(self, playID):
        # pydevd.settrace('10.252.43.52', port=53483, stdoutToServer=True, stderrToServer=True)
        for result in self.results:
            if result['play'] and result['play']['id'] == str(playID):
                return result

    def get_result_task_by_id(self, taskID):
        # pydevd.settrace('10.252.43.52', port=53483, stdoutToServer=True, stderrToServer=True)
        for result in self.results:
            for task in result['tasks']:
                if task['task']['id'] == str(taskID):
                    return task

    def v2_playbook_on_play_start(self, play):
        new_play = self._new_play(play)

        # variable_manager = play.get_variable_manager()
        # variable_manager.extra_vars = {'new_var': 'new_value'}
        if not self.get_result_play_by_id(play._uuid):
            self.results.append(new_play)

        # self.custom_print(new_play)
        self.update_ozone_ansible_object('Running')

        self.defaultCallback.v2_playbook_on_play_start(play)
        super(CallbackModule, self).v2_playbook_on_play_start(play)

    def v2_playbook_on_task_start(self, task, is_conditional, host=None):
        new_task = self._new_task(task, host)
        task_play = self.get_result_play_by_id(task._parent._play._uuid)
        if 'end_time' in task_play:
            del task_play['end_time']
        if task_play:
            if not self.get_result_task_by_id(task._uuid):
                task_play['tasks'].append(new_task)
        else:
            self._display.display(
                "Ozone Callback Plugin error - Cannot find play with ID %s" % task._parent._play._uuid,
                color=C.COLOR_ERROR)

        # self.results[-1]['tasks'].append(new_task)

        # os.environ["OZONE_KILL_FLAG"] = "KILL_JOB"

        # self.custom_print(new_task)
        self.defaultCallback.v2_playbook_on_task_start(task, is_conditional)
        self.update_ozone_ansible_object('Running')
        super(CallbackModule, self).v2_playbook_on_task_start(task, is_conditional)

    def v2_playbook_on_handler_task_start(self, task):
        self.v2_playbook_on_task_start(task, None)

    def update_task_result(self, result, status):
        host = result._host

        # MongoDB doesn't like "." or "$" in fields. Replacing them
        # In addition take a copy of result object as it is modified by the defaultCallback
        try:
            processed_results = self.replaceDotInKey(copy.deepcopy(result._result))
        except Exception as e:
            self._display.display(
                'Error replacing dots/dollar signs in result data %s' % e,
                color=C.COLOR_ERROR)
            processed_results = copy.deepcopy(result._result)

        # Strip invocation details from results. They contain sensitive data and need not be stored in results.
        self.cleanData(processed_results)
        processed_results['status'] = status
        task = self.get_result_task_by_id(result._task._uuid)

        # Remove results from processed_results. Will be added on item results
        if 'results' in processed_results:
            del processed_results['results']

        processed_results['end_time'] = int(time.time()) * 1000

        task_play = self.get_result_play_by_id(result._task._parent._play._uuid)
        task_play['end_time'] = int(time.time()) * 1000

        # print("Trying to connec to pydev 2")
        # pydevd.settrace('10.97.69.199', port=53483, stdoutToServer=True, stderrToServer=True)

        clean_hostname = self.replaceDotInKey(host.name)

        if task:
            if clean_hostname in task['hosts']:
                task['hosts'][clean_hostname].update(processed_results)
            else:
                task['hosts'][clean_hostname] = processed_results
        else:
            self._display.display(
                "Ozone Callback Plugin error - Cannot find Task with ID %s" % result._task._uuid,
                color=C.COLOR_ERROR)

        self.update_overall_task_status(task)
            # self.results[-1]['tasks'][-1]['hosts'][self.replaceDotInKey(host.name)] = processed_results
            # self.custom_print(self.results[-1]['tasks'][-1])

    def update_task_item_result(self, result, status):
        host = result._host

        # MongoDB doesn't like "." or "$" in fields. Replacing them
        # In addition take a copy of result object as it is modified by the defaultCallback
        try:
            processed_results = self.replaceDotInKey(copy.deepcopy(result._result))
        except Exception as e:
            self._display.display(
                'Error replacing dots/dollar signs in result data %s' % e,
                color=C.COLOR_ERROR)
            processed_results = copy.deepcopy(result._result)

        # Strip invocation details from results. They contain sensitive data and need not be stored in results.
        self.cleanData(processed_results)
        processed_results['status'] = status
        task = self.get_result_task_by_id(result._task._uuid)

        if task:
            if 'results' not in task['hosts'][self.replaceDotInKey(host.name)]:
                task['hosts'][self.replaceDotInKey(host.name)]['results'] = []

            task['hosts'][self.replaceDotInKey(host.name)]['results'].append(processed_results)
        else:
            self._display.display(
                "Ozone Callback Plugin error - Cannot find Task with ID %s" % result._task._uuid,
                color=C.COLOR_ERROR)

        self.update_overall_task_status(task)
            # self.results[-1]['tasks'][-1]['hosts'][self.replaceDotInKey(host.name)] = processed_results
            # self.custom_print(self.results[-1]['tasks'][-1])

    def v2_runner_on_ok(self, result, **kwargs):
        # pydevd.settrace('10.97.69.199', port=53483, stdoutToServer=True, stderrToServer=True)
        status = result._result and 'changed' in result._result and result._result['changed'] and 'Success' or 'Complete'

        # Print output to console as normal Ansible
        self.defaultCallback.v2_runner_on_ok(result)

        self.update_task_result(result, status)

        # Send message to Task Status Processor to update Ozone Database with results
        self.update_ozone_ansible_object('Running')

        super(CallbackModule, self).v2_runner_on_ok(result)

    def v2_runner_on_failed(self, result, **kwargs):
        # Print output to console as normal Ansible
        self.defaultCallback.v2_runner_on_failed(result)

        self.update_task_result(result, 'Failed')

        # Send message to Task Status Processor to update Ozone Database with results
        self.update_ozone_ansible_object('Running')

        super(CallbackModule, self).v2_runner_on_failed(result)

    def v2_runner_on_unreachable(self, result, **kwargs):
        # Print output to console as normal Ansible
        self.defaultCallback.v2_runner_on_unreachable(result)

        self.update_task_result(result, 'Unreachable')

        # Send message to Task Status Processor to update Ozone Database with results
        self.update_ozone_ansible_object('Running')

        super(CallbackModule, self).v2_runner_on_failed(result)

    def v2_runner_on_skipped(self, result, **kwargs):
        # Print output to console as normal Ansible
        self.defaultCallback.v2_runner_on_skipped(result)

        self.update_task_result(result, 'Skipped')

        # Send message to Task Status Processor to update Ozone Database with results
        self.update_ozone_ansible_object('Running')

        super(CallbackModule, self).v2_runner_on_failed(result)

    def v2_runner_item_on_ok(self, result):
        # pydevd.settrace('10.252.11.36', port=53483, stdoutToServer=True, stderrToServer=True)
        status = result._result and 'changed' in result._result and result._result['changed'] and 'Success' or 'Complete'
        self.update_task_item_result(result, status)

        # Send message to Task Status Processor to update Ozone Database with results
        self.update_ozone_ansible_object('Running')

        self.defaultCallback.v2_runner_on_ok(result)

    def v2_runner_item_on_failed(self, result):

        self.update_task_item_result(result, 'Failed')

        # Send message to Task Status Processor to update Ozone Database with results
        self.update_ozone_ansible_object('Running')

        self.defaultCallback.v2_runner_item_on_failed(result)

    def v2_runner_retry(self, result):
        temp_result = copy.deepcopy(result)

        result_task = self.get_result_task_by_id(result._task._uuid)
        start_time = result_task['hosts'][self.replaceDotInKey(result._host.name)]['start_time']

        temp_result._host.name += " - Attempt (%d of %d)" % (temp_result._result['attempts'], result._result['retries'])
        temp_result._result['start_time'] = start_time

        result_task['hosts'][self.replaceDotInKey(result._host.name)]['start_time'] = int(time.time()) * 1000

        self.update_task_result(temp_result, 'Failed')

        # Send message to Task Status Processor to update Ozone Database with results
        self.update_ozone_ansible_object('Running')

        msg = "FAILED - RETRYING: %s (%d retries left)." % (
        result._task, result._result['retries'] - result._result['attempts'])
        if (
                self._display.verbosity > 2 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += "Result was: %s" % self._dump_results(result._result)
        self._display.display(msg, color=C.COLOR_WARN)

        self._display.banner(
            "Failed Attempt %s - Retrying" % temp_result._task._uuid,
            color=C.COLOR_ERROR)


    def v2_runner_item_on_skipped(self, result):

        self.update_task_item_result(result, 'Skipped')

        # Send message to Task Status Processor to update Ozone Database with results
        self.update_ozone_ansible_object('Running')

        self.defaultCallback.v2_runner_item_on_skipped(result)

    def _filter_attempts(self, result_task):
        _result_task = {"hosts": {}}
        for host in result_task["hosts"]:
            if "Attempt" not in host:
                _result_task["hosts"][host] = result_task["hosts"][host]

        return _result_task

    def update_overall_task_status(self, result_task):
        try:
            overall_status = "N/A"
            states_order = ['Running', 'Failed', 'Unreachable', 'Complete', 'Success', 'Skipped']
            # fail_states = ['Failed', 'Unreachable', 'Skipped']
            # success_states = ['Ok', 'Success']

            all_states = jmespath.search('hosts.*.status', self._filter_attempts(result_task))

            for state in states_order:
                if state in all_states:
                    overall_status = state
                    break

            # if 'Running' in all_states:
            #     overall_status = 'Running'
            # else:
            #
            #     if set(all_states) & set(success_states):
            #         overall_status = 'Success'
            #
            #     if set(all_states) & set(fail_states):
            #         if overall_status in success_states:
            #             overall_status = 'Partial'
            #         else:
            #             if len(all_states) == 1:
            #                 overall_status = all_states[0]
            #             else:
            #                 overall_status = 'Failed'
            #
            result_task['status'] = overall_status
            self.update_ozone_ansible_object('Running')
        except Exception as ex:
            print("Unable to update overall task status %s" % ex)

    def v2_playbook_on_host_task_start(self, host, task, is_conditional=None):
        try:
            result_task = self.get_result_task_by_id(task._uuid)
            if host.name not in result_task['hosts']:
                result_task['hosts'][self.replaceDotInKey(host.name)] = {'status': 'Running', 'start_time': int(time.time()) * 1000}
                self.update_overall_task_status(result_task)
        except Exception as ex:
            print("Error in host task start callback %s" % ex)

    def v2_playbook_on_no_hosts_remaining(self):
        self._display.banner("NO MORE HOSTS LEFT")
        self.defaultCallback.v2_playbook_on_no_hosts_remaining()

    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""
        try:
            if self.kill_thread:
                self.kill_thread.stop()
        except Exception as ex:
            print('Error trying to stop redis kill listener %s' % ex)

        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        output = {
            'plays': self.results,
            'stats': summary
        }

        # self.results.append({'stats': summary})
        self.stats = summary
        # self.custom_print({'stats': summary})
        self.update_ozone_ansible_object('Complete')
        # print(json.dumps(output, indent=4, sort_keys=True))

        super(CallbackModule, self).v2_playbook_on_stats(stats)

    def v2_playbook_on_start(self, playbook):
        super(CallbackModule, self).v2_playbook_on_start(playbook)
