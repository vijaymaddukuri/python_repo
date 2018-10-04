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


class YAMLData(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(value, 'iteritems'):
                self.__dict__.__setitem__(key, YAMLData(**value))
            elif hasattr(value, '__iter__'):
                self.__dict__.__setitem__(key, [])

                for item in value:
                    if hasattr(item, 'iteritems'):
                        self.__dict__.__getitem__(key).append(YAMLData(**item))
                    else:
                        self.__dict__.__getitem__(key).append(item)
            else:
                self.__dict__.__setitem__(key, value)

    def __add__(self, other):
        from copy import deepcopy
        temp = None
        for key, value in other.__dict__.items():
            temp = deepcopy(self)
            temp.__dict__.__setitem__(key, value)
        return YAMLData(**temp.__dict__)
