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

import glob
import imp
import inspect
import os

from uiacore.foundation.factory.web import ITech


class TechFactory(object):
    _instance = None

    def __init__(self, plugin_dir=None):
        if plugin_dir and os.path.exists(plugin_dir):
            _plugin_dir = plugin_dir
        else:
            _cd = os.path.dirname(__file__)
            _plugin_dir = os.path.abspath(os.path.join(_cd, '../../imp/web'))

        for cls in self._find_classes(_plugin_dir):
            if cls().enabled:
                TechFactory._instance = cls()
                break

    @property
    def active(self):
        if TechFactory._instance:
            return TechFactory._instance
        else:
            raise RuntimeError('Failed to load UI Automation library')

    def _find_classes(self, plugin_dir):
        classes = []
        for py in self._find_python_files(plugin_dir):
            classes.extend(
                [cls for cls in self._import_classes(py)
                 if issubclass(cls, ITech) and cls is not ITech])

        return classes

    def _find_python_files(self, plugin_dir):
        _current_dir = os.path.realpath(plugin_dir)

        files = [os.path.abspath(_file)
                 for _file in glob.iglob(
                    os.path.join(_current_dir, '*.py'))]

        [files.extend(self._find_python_files(
                os.path.join(_current_dir, _chdir)))
         for _chdir in os.listdir(_current_dir)
         if os.path.isdir(os.path.join(_current_dir, _chdir))]

        return files

    def _import_classes(self, location):
        path, filename = os.path.split(location)
        module_name = os.path.splitext(filename)[0]

        try:
            fp, imp_loc, desc = imp.find_module(module_name, [path])
        except ImportError:
            return []

        try:
            try:
                module = imp.load_module(module_name, fp, imp_loc, desc)
            except Exception as ex:
                # raise ImportError('Failed to import plugin module')
                return []
        finally:
            if fp:
                fp.close()

        return [cls for _, cls in
                inspect.getmembers(module, predicate=inspect.isclass)]
