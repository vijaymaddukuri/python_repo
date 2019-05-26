import logging as logger
from lib.api_call import ExecuteAPICall
from lib.common import update_json
# REST Object to Call the API
restObj = ExecuteAPICall()


def create_data_center(create_datacenter_json, **json_data):
    """
    This is a function that updates the JSON
    and calls the create data center POST API
    :param  create_datacenter_json: The name of the JSON file
    :param: **json_data: The JSON data that needs to be updated
    :return  datacenter_id: The ID of the created datacenter
    """
    for key, value in json_data.items():
        update_json(create_datacenter_json, key, value)
    response = restObj.api_call("POST", "", create_datacenter_json)
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 202:
        logger.info("Data center created")
        return response.json()['id']
    else:
        logger.error("Request Failed")


def validate_data_center_is_available(datacenter_id):
    """
    This is a function that checks if the datacenter
    is available or not
    :param  datacenter_id: The ID of the datacenter
    :return: True: True if the datacenter is available
    """
    api_suffix = datacenter_id
    response = restObj.api_call("GET", api_suffix, "")
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 200:
        assert(response.json()['metadata']['state'] == "AVAILABLE"), "DATACENTER is NOT available"
        logger.info("DATACENTER is available")
        return True
    else:
        logger.error("Request Failed")


def create_server(datacenter_id, create_server_json, **json_data):
    """
    This is a function that updates the JSON
    and calls the create server POST API
    :param: datacenter_id: The ID of the datacenter
    :param  create_server_json: The name of the JSON file
    :param: **json_data: The JSON data that needs to be updated
    :return  server_id: The ID of the created server
    """
    for key, value in json_data.items():
        update_json(create_server_json, key, value)
    api_suffix = "{}/servers".format(datacenter_id)
    response = restObj.api_call("POST", api_suffix, create_server_json)
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 202:
        logger.info("Created Server")
        return response.json()['id']
    else:
        logger.info("Request Failed")


def update_server(datacenter_id, server_id, update_server_json, **json_data):
    """
    This is a function that updates the JSON
    and calls the update server API
    :param: datacenter_id: The ID of the datacenter
    :param  update_server_json: The name of the JSON file
    :param: **json_data: The JSON data that needs to be updated
    :return  True/False: True/False depending on the status of the request
    """
    api_suffix = "{}/servers/{}".format(datacenter_id, server_id)
    response = restObj.api_call("PATCH", api_suffix, update_server_json)
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 202:
        logger.info("Updated Server")
        return True
    else:
        logger.info("Request Failed")
        return False


def validate_server_configuration(datacenter_id, server_id, **json_data):
    """
    This is a function that validates the server configuration
    :param: datacenter_id: The ID of the datacenter
    :param: server_id: The ID of the server
    :param: **json_data: The JSON data that needs to be updated
    :return  True: If actual-expected key/value match
    """
    api_suffix = "{}/servers/{}".format(datacenter_id, server_id)
    response = restObj.api_call("GET", api_suffix, "")
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 200:
        json = response.json()
        for key, value in json_data.items():
            assert str(json['properties'][key]) == str(value), "Actual Value of {} is {} doesn't match Expected value" \
                                                               " {}".format(key, json['properties'][key], value)
            return True
    else:
        logger.info("Request Failed")


def create_lan(datacenter_id, create_lan_json, **json_data):
    """
    This is a function that updates the JSON
    and calls the Create LAN API
    :param: datacenter_id: The ID of the datacenter
    :param: create_lan_json: Name of the JSON file
    :param: **json_data: The JSON data that needs to be updated
    :return lan_id: The ID of the LAN created
    """
    for key, value in json_data.items():
        update_json(create_lan_json, key, value)
    api_suffix = "{}/lans".format(datacenter_id)
    response = restObj.api_call("POST", api_suffix, create_lan_json)
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 202:
        logger.info("Created Lan")
        return response.json()['id']
    else:
        logger.error("Request Failed")


def validate_lan_is_available(datacenter_id, lan_id):
    """
    This is a function that checks if the LAN
    is available or not
    :param  datacenter_id: The ID of the datacenter
    :param  lan_id: The ID of the LAN
    :return: True: True if the LAN is available
    """
    api_suffix = "{}/lans/{}".format(datacenter_id, lan_id)
    response = restObj.api_call("GET", api_suffix, "")
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 200:
        assert (response.json()['metadata']['state'] == "AVAILABLE"), "LAN is NOT available"
        logger.info("LAN is available")
        return True
    else:
        logger.error("Request Failed")


def create_nic(datacenter_id, server_id, create_nic_json, **json_data):
    """
    This is a function that updates the JSON
    and calls the create NIC API
    :param: datacenter_id: The ID of the datacenter
    :param: server_id: The ID of the server
    :param: create_nic_json: Name of the JSON file
    :param: **json_data: The JSON data that needs to be updated
    :return nic_id: The ID of the NIC created
    """
    for key, value in json_data.items():
        update_json(create_nic_json, key, value)
    api_suffix = "{}/servers/{}/nics".format(datacenter_id, server_id)
    response = restObj.api_call("POST", api_suffix, create_nic_json)
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 202:
        logger.info("Created NIC")
        return response.json()['id']
    else:
        logger.error("Request Failed")


def validate_nic_is_available(datacenter_id, server_id, nic_id):
    """
    This is a function that checks if the NIC
    is available or not
    :param  datacenter_id: The ID of the datacenter
    :param  server_id: The ID of the server
    :param  nic_id: The ID of the NIC
    :return: True: True if the NIC is available
    """
    api_suffix = "{}/servers/{}/nics/{}".format(datacenter_id, server_id, nic_id)
    response = restObj.api_call("GET", api_suffix, "")
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 200:
        assert (response.json()['metadata']['state'] == "AVAILABLE"), "NIC is NOT available"
        logger.info("NIC is available")
        return True
    else:
        logger.error("Request Failed")


def delete_data_center(data_center_id):
    """
    This is a function that deletes the datacenter
    :param  datacenter_id: The ID of the datacenter
    """
    api_suffix = data_center_id
    response = restObj.api_call("DELETE", api_suffix, "")
    logger.info("Status Code : {}".format(response.status_code))
    if response.status_code == 202:
        logger.info("Deleted datacenter")
    else:
        logger.error("Request Failed")

