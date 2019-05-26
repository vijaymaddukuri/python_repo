from os.path import dirname, abspath
from robot.api import logger
from shutil import copyfile

import csv
import re
import sys
import yaml


current_dir = dirname(dirname(abspath(__file__)))


class CsvToYamlConvertor:
    """
    Take the CSV input and covert it into yaml format.
    """
    def __init__(self, service, yaml_file_path, csv_file_path):
        """
        :param service: TAS or Middlewware or worker or deployment
        :param yaml_file_path: Base YAML file name along with the location
        :param csv_file_path:  CSV file name  with the location
        """

        self.yaml_file_path = yaml_file_path

        # Open our data file in read-mode.
        self.csvfile = open(csv_file_path, 'r')

        # Save a CSV Reader object.
        self.datareader = csv.reader(self.csvfile, delimiter=',', quotechar='"')

        # Service name
        self.service = service

        # Empty array for data headings, which we will fill with the first row from our CSV.
        self.data_headings = []

    def load_yaml_file(self, filename):
        """
        load YAML file

        In case of any error, this function calls sys.exit(1)
        :param filename: YAML filename along with the location
        :return: YAML as dict
        """
        try:
            with open(filename, 'r') as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    logger.error(exc)
                    sys.exit(1)
        except IOError as e:
            logger.error(e)
            sys.exit(1)

    def update_yaml_data(self, myYaml, key, value, append_mode=False):
        """
        Set or add a key to given YAML data. Call itself recursively.
        :param myYaml: YAML data to be modified
        :param key: key as array of key tokens
        :param value: value of any data type
        :param append_mode default is False
        :return: modified YAML data
        """
        if len(key) == 1:
            if not append_mode or not key[0] in myYaml:
                myYaml[key[0]] = value
            else:
                if type(myYaml[key[0]]) is not list:
                    myYaml[key[0]] = [myYaml[key[0]]]
                print([myYaml[key[0]]])
                if value not in [myYaml[key[0]]]:
                    myYaml[key[0]].append(value)
        else:
            if not key[0] in myYaml or type(myYaml[key[0]]) is not dict:
                myYaml[key[0]] = {}
            myYaml[key[0]] = self.update_yaml_data(myYaml[key[0]], key[1:], value, append_mode)
        return myYaml

    def rm_yaml_data(self, myYaml, key):
        """
        Remove a key and it's value from given YAML data structure.
        No error or such thrown if the key doesn't exist.
        :param myYaml: YAML data to be modified
        :param key: key as array of key tokens
        :return: modified YAML data
        """
        if len(key) == 1 and key[0] in myYaml:
            del myYaml[key[0]]
        elif key[0] in myYaml:
            myYaml[key[0]] = self.rm_yaml_data(myYaml[key[0]], key[1:])
        return myYaml

    def save_yaml(self, data, yaml_file):
        """
        Saves given YAML data to file and upload yaml file to remote machine
        :param data: YAML data
        :param yaml_file: Location to save the yaml file
        """
        try:
            with open(yaml_file, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)
        except IOError as e:
            logger.error(e)
            sys.exit(1)

    def convert_csv_to_yaml(self):
        """
        Update the yaml file and save it
        """
        # Loop through each row...
        for row_index, row in enumerate(self.datareader):
            # If this is the first row, populate our data_headings variable.
            if row_index == 0:
                data_headings = row

            # Othrwise, create a YAML file from the data in this row...
            else:
                # Create a new config.yaml with filename based on index number (Tenant ID) of our current row
                # and service
                filename = str(row[0]) + '_' + self.service.lower() + '_config' + '.yaml'
                print(filename)
                # copyfile(self.yaml_file_path, filename)
                readyamldata = self.load_yaml_file(filename)

                # Empty string that we will fill with YAML formatted text based on data extracted from our CSV.
                yaml_text = ""

                # Loop through each cell in this row...
                for cell_index, cell in enumerate(row):

                    # Compile a line of YAML text from our headings list and the text of the current cell,
                    # followed by a linebreak.
                    # Heading text is converted to lowercase. Spaces are converted to underscores and hyphens
                    # are removed.
                    # In the cell text, line endings are replaced with commas.
                    cell_heading = data_headings[cell_index].replace(" ", "_").replace("-", "")

                    # Create the list of keys
                    cell_items = cell_heading.split('.')

                    if len(cell_items) == 1:
                        cell_keys = [cell_heading]
                    else:
                        cell_keys = cell_items

                    # Get the cell value
                    cell_value = cell.replace("\n", ", ")

                    # Update the data in yaml format
                    set_value = self.update_yaml_data(readyamldata, cell_keys, cell_value)
                    # Save the yaml data into a file
                    self.save_yaml(set_value, filename)

                    # Open the above yaml file to update the list formatted data
                    f = open(filename, 'r')
                    f = f.read()

                    # Convert the data into list format using regex
                    final = (re.sub(r'(\'[0-9]\'\:\s+)', '- ', str(f)))

                    # Save the file
                    with open(filename, 'w') as f:
                        f.write(final)
        # Close the CSV
        self.csvfile.close()

# Sample Execution
yamlObj = CsvToYamlConvertor('tas', r'C:\Users\madduv\ONBFactory\config.yaml', r'C:\Users\madduv\Downloads\inputfile.csv')
yamlObj.convert_csv_to_yaml()
