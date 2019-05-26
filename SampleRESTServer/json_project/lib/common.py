import logging
import json
from os.path import dirname, abspath, join
base_dir = dirname(dirname(abspath(__file__)))


def get_json(file):
    """
    This function is a generic function that fetches JSON data from a file
    :param:  file: The path of the JSON file
    :return: json_data: The JSON data from the file
    """
    try:
        with open(file, 'rb') as f:
            json_data = json.load(f)
        return json_data
    except (IOError, ValueError) as e:
        logging.debug("Exception while reading file for json, "
                      "Exception: %s" % e)
        return None


def update_json(json_file_name, key, value):
    """
    This function is a generic function that updates  values by key in a JSON file
    :param: json_file_name: Name of the JSON file
    :param: key: the key whose value needs to be updated
    :param: value: the new value that should be updated
    :return: json_data: The JSON data from the file
    """
    json_path = join(base_dir, 'json', json_file_name)
    file = get_json(json_path)
    file['properties'][key] = value
    try:
        with open(json_path, 'w') as f:
            json.dump(file, f, indent=4)
    except (IOError, ValueError) as e:
        logging.debug("Exception while reading file for json, "
                      "Exception: %s" % e)
        return None
