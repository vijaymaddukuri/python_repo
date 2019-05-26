import logging

from common.constants import BACKUP_LOG_ID
from common.exceptions import TASException

from backup.RestApiTemplate import RestApiTemplate
from backup.constants import (BACKUP_ERRORS,
                              NW_CLIENT_URL,)

logger = logging.getLogger(__name__)


class Networker:
    """
    This Class exposes the Basic functionality of Networker
    API and the defined functions are reusable by higher layers
    """
    nw_base_url = '/nwrestapi/v2/global'

    def __init__(self, username, password, url):
        self.rat = RestApiTemplate(username, password, url)

    def get_all_clients(self):
        """
        :return: returns the List of all Clients as a JSON Object
        """
        logger.info("{} Inside: get_all_clients".format(BACKUP_LOG_ID))
        all_client = self.rat.send_request('GET',
                                     self.nw_base_url + '/clients/', {})
        logger.debug("{} Response of get_all_clients: {}".format(BACKUP_LOG_ID, all_client))
        logger.info("{} Exit: get_all_clients".format(BACKUP_LOG_ID))
        return all_client

    def get_client(self, hostname):
        """
        :param hostname: Hostname of the Networker Client VM
        :return: Returns a client JSON object filtered using the resource ID
        """
        logger.info("{} Inside: get_client".format(BACKUP_LOG_ID))
        logger.debug("{} get_client: parameters: {}".format(BACKUP_LOG_ID, hostname))
        client = self.rat.send_request('GET', self.nw_base_url + '/clients/?q=hostname:' + hostname, {})
        logger.debug("{} Response of get_client: {}".format(BACKUP_LOG_ID, client))
        if "error_code" in client:
            logger.info("{} Exit: get_client".format(BACKUP_LOG_ID))
            return client
        elif 'clients' in client and len(client['clients']) > 0:
            logger.info("{} Exit: get_client".format(BACKUP_LOG_ID))
            return client['clients'][0]
        logger.info("{} Exit: get_client".format(BACKUP_LOG_ID))
        return {}

    def create_client(self, hostname, save_sets):
        """
        :param hostname: FQDN of the Networker Client VM
        :param save_sets:List of Directories to be backup
        :return: Creates a new Client Object in Networker Server
                 based on the inputs provided
        """
        logger.info("{} Inside: create_client".format(BACKUP_LOG_ID))
        logger.debug("{} create_client: parameters: {} {}".format(BACKUP_LOG_ID, hostname, save_sets))
        body = {'hostname': hostname, 'saveSets': save_sets}
        client = self.rat.send_request('POST', self.nw_base_url + '/clients/', body)
        logger.debug("{} Response of create_client: {}".format(BACKUP_LOG_ID, client))
        logger.info("{} Exit: create_client".format(BACKUP_LOG_ID))
        return client

    def get_client_resource_id(self, hostname):
        """
        :param hostname: FQDN of the Networker Client VM
        :return: Fetches the Client resource ID based on the hostname
        """
        logger.info("{} Inside: get_client_resource_id".format(BACKUP_LOG_ID))
        logger.debug("{} get_client_resource_id: parameter: {}".format(BACKUP_LOG_ID, hostname))
        clients_list = self.get_all_clients()
        if "error_code" in clients_list:
            logger.info("{} Exit: get_client_resource_id".format(BACKUP_LOG_ID))
            return clients_list

        for client in clients_list['clients']:
            if client['hostname'] == hostname:
                resource_id = client['resourceId']['id']
                logger.debug("{} Response of get_client_resource_id:{}".format(BACKUP_LOG_ID, resource_id))
                logger.info("{} Exit: get_client_resource_id".format(BACKUP_LOG_ID))
                return resource_id
        logger.info("{} Exit: get_client_resource_id".format(BACKUP_LOG_ID))
        return 0

    def get_protection_group(self, pg_name):
        """
        :param pg_name: name of the protection Group
        :return: Fetch the Protection Group object
                 based on the name
        """
        logger.info("{} Inside: get_protection_group".format(BACKUP_LOG_ID))
        logger.debug("{} get_protection_group: parameters: {}".format(BACKUP_LOG_ID, pg_name))
        pg = self.rat.send_request('GET', self.nw_base_url + '/protectiongroups/' +
                                     pg_name, {})
        logger.debug("{} Response of get_protection_group: {}".format(BACKUP_LOG_ID, pg))
        logger.info("{} Exit: get_protection_group".format(BACKUP_LOG_ID))
        return pg

    def add_client_to_protection_group(self, pg_name, client):
        """
        :param pg_name:name of the protection Group
        :param client: Client Object in
        :return: Adds the client to the protection group based on its resource ID
        """
        logger.info("{} Inside: add_client_to_protection_group".format(BACKUP_LOG_ID))
        logger.debug("{} add_client_to_protection_group: parameters : {} {}".format(BACKUP_LOG_ID, pg_name, client))
        resource_id = 0
        if "resourceId" in client.keys():
            resource_id = client["resourceId"]["id"]
        if "protectionGroups" in client.keys():
            for pf in client["protectionGroups"]:
                if pf != pg_name:
                    self.remove_client_from_protection_group(resource_id, pf)

        pg = self.get_protection_group(pg_name)
        logger.debug("{} Response from get_protection_group: {}".format(BACKUP_LOG_ID, pg))
        if "error_code" in pg:
            logger.info("{} Exit: add_client_to_protection_group".format(BACKUP_LOG_ID))
            return pg
        if resource_id not in pg['workItems']:
            pg['workItems'].append(resource_id)
            add_pg_result = self.rat.send_request('PUT', self.nw_base_url + '/protectiongroups/' + pg_name, pg)
            logger.debug("{} Response of add_client_to_protection_group: {}".format(BACKUP_LOG_ID, add_pg_result))
            logger.info("{} Exit: add_client_to_protection_group".format(BACKUP_LOG_ID))
            return add_pg_result
        logger.info("{} Exit: add_client_to_protection_group".format(BACKUP_LOG_ID))
        return {"error_code": 400, "error_message": "Client already added to the protection Group"}

    def get_backup_history_of_client(self, resource_id):
        """
        :param resource_id: Resource_ID assigned to the
                            Networker Client VM
        :return: Fetches the backup history of client
        """
        logger.info("{} Inside: get_backup_history_of_client".format(BACKUP_LOG_ID))
        logger.debug("{} get_backup_history_of_client: parameters : {}".format(BACKUP_LOG_ID, resource_id))
        bkup_client = self.rat.send_request('GET', self.nw_base_url + '/clients/' + resource_id +
                                     '/backups', {})
        logger.debug("{} Response of get_backup_history_of_client: {}".format(BACKUP_LOG_ID, bkup_client))
        logger.info("{} Exit: get_backup_history_of_client".format(BACKUP_LOG_ID))
        return bkup_client

    def remove_client_from_protection_group(self, resource_id,
                                            pg_name):
        """
        :param resource_id: Resource_ID assigned to the Networker Client VM
        :param pg_name: name of the protection Group
        :return: Removes the client from the protection group based on the inputs
        """
        logger.info("{} Inside: remove_client_from_protection_group".format(BACKUP_LOG_ID))
        logger.debug(
            "{} remove_client_from_protection_group: parameters : {} {}".format(BACKUP_LOG_ID, resource_id, pg_name))
        pg = self.get_protection_group(pg_name)
        logger.debug("{} Response from get_protection_group: {} ".format(BACKUP_LOG_ID, pg))
        if "error_code" in pg:
            logger.info("{} Exit: remove_client_from_protection_group".format(BACKUP_LOG_ID))
            return pg
        if pg['workItems'] and resource_id in pg['workItems']:
            pg['workItems'].remove(resource_id)
        remove_pg_result = self.rat.send_request('PUT', self.nw_base_url + '/protectiongroups/' +
                                     pg_name, pg)
        logger.debug("{} Response of remove_client_from_protection_group: {} ".format(BACKUP_LOG_ID, remove_pg_result))
        logger.info("{} Exit: remove_client_from_protection_group".format(BACKUP_LOG_ID))
        return remove_pg_result

    def change_backup_state(self, client_details, task_id, state=True):
        """
        :param client_details: VM client details from Networker
        :param task_id: task id created for service request
        :param state: True or False status to be updated on schedule backup
        :return: Changes status and returns response.
        """
        try:
            if 'resourceId' in client_details and 'id' in client_details['resourceId']:
                resource_id = client_details['resourceId']['id']
            else:
                err_code = "BACKUP016_CLIENT_INFORMATION_NOT_FOUND"
                err_message = BACKUP_ERRORS[err_code]
                err_trace = ""
                raise TASException(err_code, err_message, err_trace)

            logger.info("{} Inside: change_backup_state".format(BACKUP_LOG_ID))
            logger.debug(
                "{} change_backup_state: parameters : {} {}".format(BACKUP_LOG_ID, resource_id, task_id))
            data = {'scheduledBackup': state}
            if state:
                data['comment'] = '[Task-ID: {}] Scheduled Backup enabled after VM Start.'.format(task_id)
            else:
                data['comment'] = '[Task-ID: {}] Scheduled Backup disabled before VM Stop.'.format(task_id)
            update_backup_resp = self.rat.send_request('PUT', NW_CLIENT_URL +
                                         resource_id, data)
            logger.debug("{} Response of change_backup_state: {} ".format(BACKUP_LOG_ID, update_backup_resp))
            logger.info("{} Exit: change_backup_state".format(BACKUP_LOG_ID))
            return update_backup_resp
        except TASException as e:
            raise
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {}".format(BACKUP_LOG_ID, message))
            raise Exception(message)

    def delete_client(self, resource_id):
        """
        :param resource_id: Resource_ID assigned to the Networker Client VM
        :return: Deletes Client Object from the Networker Server
        """
        logger.info("{} Inside: delete_client".format(BACKUP_LOG_ID))
        logger.debug("{} delete_client: parameters: {}".format(BACKUP_LOG_ID, resource_id))
        del_client = self.rat.send_request('DELETE', self.nw_base_url + '/clients/' +
                                     resource_id, {})
        logger.debug("{} Response of delete_client: {}".format(BACKUP_LOG_ID, del_client))
        logger.info("{} Exit: delete_client".format(BACKUP_LOG_ID))
        return del_client

    def is_full(self, max_clients, max_jobs):
        """
        :parm max_clients: maximum number of clients a Netwoker server may have before it is considered full
        :parm max_jobs: maximum number of jobs a Netwoker server may have before it is considered full
        :return: True if the Networker is full
        """
        clients = self.rat.send_request('GET', self.nw_base_url + '/clients', {})
        if not isinstance(clients, dict):
            logger.error('{} response for client list is not a dict, got {}'.format(BACKUP_LOG_ID, clients))
            return True
        try:
            logger.debug("{} Response received for clients API call. Clients count {}".format(BACKUP_LOG_ID, int(clients['count'])))
            logger.info("{} Threshold clients count/maximum clients count {}/{} for the networker {}".format(BACKUP_LOG_ID,
                                                                                int(clients['count']), max_clients, self.rat.url))
            if int(clients['count']) >= max_clients:
                return True
        except (KeyError, ValueError) as e:
            logger.error('{} Error getting count from client list: {}. Response received {}'.format(BACKUP_LOG_ID, e, clients))
            return True

        jobs = self.rat.send_request('GET', self.nw_base_url + '/jobs', {})
        if not isinstance(jobs, dict):
            logger.error('{} response for job list is not a list, got {}'.format(BACKUP_LOG_ID, jobs))
            return True

        try:
            logger.debug("{} Response received for jobs API call. Jobs count {}".format(BACKUP_LOG_ID, int(jobs['count'])))

            logger.info("{} Threshold jobs count/maximum jobs count {}/{} for the networker {}".format(BACKUP_LOG_ID, int(jobs['count']),
                                                                                  max_jobs, self.rat.url))
            if int(jobs['count']) >= max_jobs:
                return True
        except (KeyError, ValueError) as e:
            logger.error('{} Error getting count from job list: {}. Response received {}'.format(BACKUP_LOG_ID, e, jobs))
            return True

        return False

    def enable_backup(self, client_hostname, client_savesets, pg_name):
        """
        :param networker_username: Username for Networker Server
        :param networker_password: Password for Networker Server
        :param networker_url: URL of Networker Server
        :param client_hostname: FQDN of the VM for which Backup needs to be enabled
        :param client_savesets: List of the directories that need to be backed up.
        :param pg_name: Name of the Protection group
        :return: Returns the status as a Json Array
        """
        logger.info("{} Inside: enable_backup".format(BACKUP_LOG_ID))
        logger.debug(
            "{} enable_backup: parameters : {} {} {} ".format(BACKUP_LOG_ID, client_hostname, client_savesets, pg_name))
        all_steps = []
        # Step 1: Check whether client already present. If not, Client is created
        client = self.get_client(client_hostname)
        # If Error occurred while Fetching Client
        if type(client) is dict and "error_code" in client:
            step1_return = {"step": 1,
                            "description": "Create the client",
                            "result": "An error occurred",
                            "error": client
                            }
            all_steps.append(step1_return)
            logger.info("{} Exit: enable_backup".format(BACKUP_LOG_ID))
            return all_steps

        # Else If Client not present
        elif not client:
            status = self.create_client(client_hostname, client_savesets)
            if "error_code" in status:
                step1_return = {"step": 1,
                                "description": "Create the client",
                                "result": "An error occurred",
                                "error": status
                                }
                all_steps.append(step1_return)
                logger.info("{} Exit: enable_backup".format(BACKUP_LOG_ID))
                return all_steps
            else:
                client = self.get_client(client_hostname)
                step1_return = {"step": 1,
                                "description": "Create the client",
                                "result": "Client created with Resource ID " + client["resourceId"]["id"],
                                "error": {}
                                }

        # Else If Client Present
        else:
            step1_return = {"step": 1,
                            "description": "Create the client",
                            "result": "Client already configured. Moving to the next step",
                            "error": {}
                            }

        all_steps.append(step1_return)

        # Step 2: Check whether Client already added to Protection. if not, Add the Client to Protection Group
        status = self.add_client_to_protection_group(pg_name, client)
        if "error_code" in status:
            step2_return = {"step": 2,
                            "description": "Add the client to the Protection Group",
                            "result": "An error occurred",
                            "error": status
                            }
            all_steps.append(step2_return)
            logger.info("{} Exit: enable_backup".format(BACKUP_LOG_ID))
            return all_steps

        else:
            step2_return = {"step": 2,
                            "description": "Add the client to the Protection Group",
                            "result": "Client added to the protection group.",
                            "error": {}
                            }

        all_steps.append(step2_return)
        logger.info("{} Exit: enable_backup".format(BACKUP_LOG_ID))
        return all_steps
