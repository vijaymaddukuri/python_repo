import yaml


def get_config(appliance, param, yaml_file_path):
    """This function gives the yaml value corresponding to the parameter
    sample Yaml file
        xstream_details:
            xtm_host: 10.100.26.90
    :param appliance: The header name as mentioned in the yaml file (ex:xstream_details)
    :param param: The parameter name who's value is to be determined (ex: xtm_host)
    :param yaml_file_path: Path of yaml file, Default will the config.yaml file
    :return: value corresponding to the parameter in yaml file
    :except: Exception while opening or loading the file
    """
    try:
        with open(yaml_file_path, 'r') as f:
            doc = yaml.load(f)
        param_value = doc[appliance][param]
        if param_value == "":
            message = 'Value is not updated for the parameter:{} in the yaml config file'\
                .format(param)
            raise Exception(message)
        return param_value
    except Exception as ex:
        message = "Exception: An exception occured: {}".format(ex)
        raise Exception(message)

def print_results(result_dict):
    print('\nResult Summary:')
    print("----------------------------------------------")
    print("Component" + 20 * " " + "Status")
    print("----------------------------------------------")
    for result in result_dict:
        gap = 29 - len(result)
        space = ' ' * gap
        print(result + space + result_dict[result])
        print("\n")
    count = 0
    passed = [i for i in result_dict.values() if i == "PASS"]
    print("----------------------------------------------")
    print("Total Testcases: {}  PASSED:  {}  FAILED: {}".format(len(result_dict), len(passed),
                                                                len(result_dict) - len(passed)))
    print('\n')