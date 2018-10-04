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


class Context(object):
    def __init__(self, ctx=None):
        if issubclass(type(ctx), Context):
            self.__dict__.update(**ctx.__dict__)
        else:
            self._init_context(ctx)

    def _init_context(self, ctx):
        raise NotImplementedError(
            'Initializing context is not implemented')

    def __getitem__(self, item):
        if hasattr(self, str(item)):
            return getattr(self, str(item))
        else:
            return None

    def __setitem__(self, key, value):
        self.__setitem(self, str(key), value)

        # if hasattr(self, str(key)):
        #     getattr(self, str(key)).__dict__.update(vars(value))
        # else:
        #     setattr(self, str(key), value)

    def __iter__(self):
        return vars(self).iteritems()

    def __setitem(self, node, key, value):
        if hasattr(node, key):
            self.__update_attr(node, key, value)
        else:
            setattr(node, str(key), value)

    def __update_attr(self, node, key, value):
        if hasattr(value, '__dict__'):
            for _key, _value in vars(value).iteritems():
                self.__setitem(getattr(node, key), _key, _value)
        elif hasattr(value, 'iteritems'):
            for _key, _value in value.iteritems():
                self.__setitem(getattr(node, key), _key, _value)
        elif hasattr(value, '__iter__'):
            for item in value:
                # Probably need to consider nested dict object
                getattr(node, key).append(item)
        else:
            setattr(node, key, value)
