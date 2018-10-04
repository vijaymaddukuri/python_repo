# ------------------------------------------------------------------------------
# Copyright (C) 2016-2017 DELL EMC Corporation. All Rights Reserved.

# This software contains the intellectual property of DELL EMC Corporation
# or is licensed to DELL EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of DELL  EMC.

# ------------------------------------------------------------------------------

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

import json

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'jsonp'

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)
        self.results = []

    def _new_play(self, playObject):
        return {
            'play': {
                'name': playObject.name,
                'id': str(playObject._uuid)
            },
            'tasks': [],
        }

    def _new_task(self, task):
        return {
            'task': {
                'name': task.name,
                'id': str(task._uuid)
            },
            'hosts': {},
        }

    def custom_print(self, content):
        print('--------BEGIN--------')
        #print(content)
        print(json.dumps(content, indent=4, sort_keys=True))
        print('--------END--------')

    def v2_playbook_on_play_start(self, play):
        new_play = self._new_play(play)
        self.results.append(new_play)
        self.custom_print(new_play)

    def v2_playbook_on_task_start(self, task, is_conditional):
        new_task = self._new_task(task)
        self.results[-1]['tasks'].append(new_task)
        self.custom_print(new_task)

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        self.results[-1]['tasks'][-1]['hosts'][host.name] = result._result
        self.custom_print(self.results[-1]['tasks'][-1])

    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""

        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        output = {
            'plays': self.results,
            'stats': summary
        }

        #print(json.dumps(output, indent=4, sort_keys=True))
        self.custom_print({'stats' : summary})

    v2_runner_on_failed = v2_runner_on_ok
    v2_runner_on_unreachable = v2_runner_on_ok
    v2_runner_on_skipped = v2_runner_on_ok
