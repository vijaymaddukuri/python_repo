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

import os

import yaml

from uiacore.foundation.utils import YAMLData


class ITech(object):
    @property
    def enabled(self):
        _cd = os.path.dirname(__file__)
        _cfg = os.path.abspath(os.path.join(_cd, 'default.yaml'))
        with open(_cfg) as _cfg_file:
            cfg = YAMLData(**yaml.load(_cfg_file))

        _enabled = False

        try:
            _technologies = getattr(cfg, 'ITechnology')
            _current_tech = getattr(
                _technologies, self.__class__.__name__)
            _enabled = getattr(_current_tech, 'enabled')
        except AttributeError:
            pass

        return _enabled

    def get_browser(self):
        raise NotImplementedError('Not Implemented')

    def get_element_type(self, pattern):
        raise NotImplementedError('Not Implemented')
