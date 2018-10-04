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
from .context import Context
from .model import YAMLData


class DataContext(Context):
    def __init__(self, yml_file=None, attr_name=None):
        self._attributes = ['default'] if not attr_name else [attr_name]

        super(DataContext, self).__init__(yml_file)

    def update_context(self, yml_file, attr_name=None):
        if (not yml_file) and attr_name and (not hasattr(self, attr_name)):
            if attr_name not in self._attributes:
                self._attributes.append(attr_name)
            self[attr_name] = YAMLData(**{})

        if yml_file and os.path.isfile(yml_file):
            try:
                _attr_name = attr_name or os.path.splitext(
                        os.path.split(yml_file)[-1])[0]

                if _attr_name in self._attributes:
                    index = self._attributes.index(_attr_name)
                else:
                    index = -1
                    self._attributes.append(_attr_name)

                with open(yml_file) as yml:
                    self[self._attributes[index]] = YAMLData(**yaml.load(yml))
            except IOError as ex:
                raise ex

    def _init_context(self, ctx):
        self.update_context(ctx, self._attributes[-1])
