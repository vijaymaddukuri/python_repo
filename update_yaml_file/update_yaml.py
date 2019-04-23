import yaml
import logging as logger
import sys


filepath = "C://Users//madduv//Desktop//config.yaml"


def load_yaml_from_file():
    """
    load YAML file
    In case of any error, this function calls sys.exit(1)
    :param name: path & file name
    :return: YAML as dict
    """
    try:
        with open(filepath, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.error(exc)
                sys.exit(1)
    except IOError as e:
        logger.error(e)
        sys.exit(1)


def save_yaml(data):
    """
    Saves given YAML data to file
    :param name: file path
    :param data: YAML data
    """
    try:
        with open(filepath, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
    except IOError as e:
        logger.error(e)
        sys.exit(1)

def set_key(myYaml, key, value, append_mode=False):
    """
    Set or add a key to given YAML data. Call itself recursively.
    :param myYaml: YAML data to be modified
    :param key: key as array of key tokens
    :param value: value of any data type
    :param append_mode default is False
    :return: modified YAML data
    """
    # self.log("set_key {} = {} | yaml: {}".format(key, value, myYaml), debug=True)
    if len(key) == 1:
        if not append_mode or not key[0] in myYaml:
            myYaml[key[0]] = value
        else:
            if type(myYaml[key[0]]) is not list:
                myYaml[key[0]] = [myYaml[key[0]]]
            myYaml[key[0]].append(value)
    else:
        if not key[0] in myYaml or type(myYaml[key[0]]) is not dict:
            # self.log("set_key {} = {} creating item".format(key, value, myYaml), debug=True)
            myYaml[key[0]] = {}
        myYaml[key[0]] = set_key(myYaml[key[0]], key[1:], value, append_mode)
    return myYaml

readyamldata = load_yaml_from_file()
print(readyamldata)
set_value = set_key(myYaml=readyamldata, key=['nimsoft_server_details', 'NIMSOFT_HUB_IP'], value='')
save_yaml(set_value)