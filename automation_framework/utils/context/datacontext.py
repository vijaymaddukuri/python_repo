import os
import yaml

from .context import Context
from .model import YAMLData
from robot.api import logger


class DataContext(Context):
    """
    How to load data while providing yaml inputs.
    In BaseWOrkFlow.py we will define the tags to store the data
    Passes the info to the YAMLData to update the Dictionaries
    """
    def __init__(self, yml_file=None, attr_name=None):
        """
        :param yml_file: Yaml file
        :param attr_name: name of the variable to store data
        Step 1: Take the attribute name as input or use default var name
        Step 2: Take the Yaml file as input
        """
        # Step 1: Take the attribute name as input or use default var name
        self._attributes = ['default'] if not attr_name else [attr_name]

        # Step 2: Take the Yaml file as input
        super(DataContext, self).__init__(yml_file)

    def update_context(self, yml_file, attr_name=None):
        """
        Opens the Yaml file and store the data into an attribute
        Args:
        :param yml_file: Yaml file
        :param attr_name: name of the variable to store data
        :return: Dictionary with key value pairs
        Step 1: Create a data type (YAMLData) to store data
        Step 2: Open the YAML file and append the data to attribute
        Exception: Raise an exception when YAML file path is not found
        """
        # Step 1: Create a data type (YAMLData) to store data
        if (not yml_file) and attr_name and (not hasattr(self, attr_name)):
            if attr_name not in self._attributes:
                self._attributes.append(attr_name)
            self[attr_name] = YAMLData(**{})

        # Step 2: Open the YAML file and append the data to attribute
        if yml_file and os.path.isfile(yml_file):
            try:
                _attr_name = attr_name or os.path.splitext(os.path.split(yml_file)[-1])[0]

                if _attr_name in self._attributes:
                    index = self._attributes.index(_attr_name)
                else:
                    index = -1
                    self._attributes.append(_attr_name)

                with open(yml_file) as yml:
                    self[self._attributes[index]] = YAMLData(**yaml.load(yml))
            # Exception: Raise an exception when YAML file path is not found
            except IOError as ex:
                raise ex

    def _init_context(self, ctx):
        self.update_context(ctx, self._attributes[-1])