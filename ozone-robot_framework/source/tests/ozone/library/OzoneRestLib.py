from ozone.utils.service import OzoneSession
from robot.api import logger
from ozoneConstants import *
import json
import requests
import pprint


class OzoneRestLib(object):
    """
        Library for Ozone REST API Calls
    """

    def __init__(self, hostname, email, password):
        """
        :param hostname:
        :param email:
        :param password:
        """
        self._hostname = hostname
        self._email = email
        self._session = OzoneSession(email, password, hostname)

    def config_master_password(self, masterpassword):
        """
             Description: config ozone master password
             :param ozoneInitDict:
                     'host' - ip or fqdn of Ozone
                     'username' - username for Ozone
                     'password' - init password for Ozone
              param 'masterPassword' -  configured password for ozone
            :return: True or False
          """
        try:
            logger.info('Begin to config ozone master password {}'.format(self._hostname))
            url = 'https://{0}/{1}'.format(self._hostname, OZONE_CONFIG_URL)
            logger.info('URL is {}'.format(url))

            body = CONFIG_MASTER_PASSWORD_BODY
            body["masterPassword"] = masterpassword

            response = self._session.post(url, json=body)
            logger.info(response.status_code)
            if not response.ok:
                logger.error('Failed to config ozone master password')
                return False
            logger.info('The master password has been configured !')
            return True
        except Exception as err:
            logger.error('Exception while configuring ozone master password')
            logger.error(err.message)

    def config_user_password(self, username, old_password, new_password):
        """
            Description: Configures Ozone user password
            :param username: Ozone user name
            :param old_password: Ozone user old password
            :param new_password: Ozone user new password
            :return: True or False
        """
        try:
            logger.info('Begin to config ozone user password {}'.format(self._hostname))
            id = self.get_userid_by_name(username)
            url = 'https://{0}/{1}/{2}/password'.format(self._hostname, OZONE_USER_URL, id)
            logger.info('URL is {}'.format(url))

            body = CONFIG_USER_PASSWORD_BODY
            body['oldPassword'] = old_password
            body['newPassword'] = new_password

            response = self._session.put(url, json=body)
            logger.info(response.status_code)
            if response.status_code != requests.codes.no_content:
                logger.error('Failed to config user master password')
                return False
            logger.info('The user password has been configured !')
            return True
        except Exception as err:
            logger.error('Exception while configuring ozone user password')
            logger.error(err.message)

    def start_service(self):
        """
        Description: Starts Ozone service
        :return: True or False
        """
        try:
            logger.info('Begin to start system service {}'.format(self._hostname))
            url = 'https://{0}/{1}'.format(self._hostname, OZONE_SERVICE_URL)
            logger.info('URL is {}'.format(url))

            response = self._session.post(url)
            logger.info(response.status_code)
            if response.status_code != requests.codes.server_error:
                logger.error('Failed to start system service ')
                return False
            logger.info('The system has been started !')
            return True
        except Exception as err:
            logger.error('Exception while start system service!')
            logger.error(err.message)

    def is_set_master_password(self):
        """
            Description: Verifies Ozone master password
            :return: True or False
        """
        try:
            logger.info('Begin to verify ozone master password {}'.format(self._hostname))
            url = 'https://{0}/{1}'.format(self._hostname, OZONE_VERIFY_URL)
            logger.info('URL is {}'.format(url))

            response = self._session.get(url)
            logger.info(response.status_code)
            if not response.ok:
                logger.error('Failed to verify ozone master password')
                return False
            logger.info('The password has been configured successfully!')
            return True
        except Exception as err:
            logger.error('Exception while verifying ozone master password')
            logger.error(err.message)

    def is_set_user_password(self, newpassword):
        """
            Description: Verify ozone user password
        """
        try:
            self._session = OzoneSession(self._email, newpassword, self._hostname)
            return True
        except Exception as err:
            logger.error('User password is not set')
            logger.error(err.message)
            return False

    def get_userid_by_name(self, username):
        """
            Description: Get user ID by Name
            :param username: Ozone username
            :return: userid or False
        """
        try:
            logger.info('Begin to get user ID by name {}'.format(self._hostname))
            url = 'https://{}/{}'.format(self._hostname, OZONE_USER_URL)
            logger.info('URL is {}'.format(url))

            response = self._session.get(url)
            logger.info(response.status_code)
            if not response.ok:
                logger.error('Failed to get user ID by name')
                return False
            user_list = response.json()
            for user in user_list:
                if user['name'] == username:
                    return user['_id']
            return False
        except Exception as err:
            logger.error('Exception while get user id by name')
            logger.error(err.message)

    def execute_ansible_job(self, project_name, playbook):
        """
            Description: Executing Ansible Job and waiting till it completes
            :param project_name: Ozone Project Name
            :param playBook: Dictionary:
                'name' - name of playBook(String)
                'tags' - tags of playBook(List)
            :return: True or False
        """
        try:
            project = self.get_project_details_by_name(project_name)
            data = OZONE_ANSIBLE_DATA
            data['type'] = [playbook['name']]
            data['tags'] = playbook['tags']
            data['refid'] = project['_id'] + "_" + playbook['name']
            data['project'] = project
            # logger.info(data['refid'])
            # logger.info(data['project'])
            # execute ansible job
            url = 'https://{}/{}'.format(self._hostname, OZONE_EXECUTE_ANSIBLE_JOB)
            logger.info(url)
            response = self._session.post(url, json=data)
            logger.info(response.status_code)
            # logger.info(response.content)
            logger.info('Execute Playbook REST Call Response')
            pprint.pprint(response.content)
            if not response.ok:
                logger.error('Failed to execute ansible playbook {}'.format(playbook['name']))
                return False
            logger.info('Successfully execute ansible playbook {}'.format(playbook['name']))
            execution_id = response.json()['_id']
            # get job status
            url = 'https://{0}:443/{1}{2}'.format(self._hostname, OZONE_GET_ANSIBLE_JOB,
                                                  execution_id)
            logger.info(url)
            retry = True
            state = 'active'
            while state == 'active':
                response = self._session.get(url)
                if not response.ok:
                    logger.error('Failed to get ansible job status')
                    return False
                output = response.json()
                state = output['state']
                if state in ('complete', 'failed'):
                    break
            # logger.info(response.json())
            logger.info('Total Execution Status of Playbook')
            pprint.pprint(response.json())
            logger.info('Successfully get ansible job status')
            logger.info('Job status is :{}'.format(state))
            return True if state == 'complete' else False
        except Exception as err:
            logger.error("Exception while executing ansible job in Ozone")
            logger.error(err.message)
            return False

    def create_project(self, project_details):
        """
            Description: Create project in Ozone
            :param project_details - Ozone project info(Dict)
                    'name': name for project(String)
                    'type': type for project(String)
            :return True/False
        """
        try:
            url = 'https://{}/{}'.format(self._hostname, OZONE_PROJECT_URL)
            response = self._session.post(url, json=project_details)
            logger.info(response.status_code)
            logger.info(response.content)
            if response.status_code != requests.codes.created:
                logger.error('Failed to create project {}'.format(project_details['name']))
                return False
            logger.info('Successfully create project {}'.format(project_details['name']))
            return True

        except Exception as err:
            logger.error("Exception while creating project in Ozone")
            logger.error(err.message)

    def get_projectid_by_name(self, project_name):
        """
            Description: Get project id by name in Ozone
            :param project_name - Ozone project name(String)
            :return Project id(String)
            """
        try:
            url = 'https://{0}/{1}'.format(self._hostname, OZONE_PROJECT_URL)
            response = self._session.get(url)
            logger.info(response.status_code)
            # logger.info(response.content)
            if not response.ok:
                logger.error('Failed to get project')
                return False
            project_list = response.json()
            for project in project_list:
                if project['name'] == project_name:
                    project_id = project['_id']
                    logger.info('Project id of project {} is {}'.format(project_name, project_id))
                    return project_id
            logger.error('Failed to find project {}'.format(project_name))
            return False

        except Exception as err:
            logger.error("Exception while getting project id in Ozone")
            logger.error(err.message)

    def delete_project(self, project_name):
        """
            Description: Delete project by name in Ozone
            :param project_name - Ozone project name(String)
            :return True/False
            """
        try:
            project_id = self.get_projectid_by_name(project_name)
            url = 'https://{0}/{1}/{2}'.format(self._hostname, OZONE_PROJECT_URL, project_id)

            response = self._session.delete(url)
            logger.info(response.status_code)
            logger.info(response.content)
            if response.status_code != requests.codes.no_content:
                logger.error('Failed to delete project {}'.format(project_name))
                return False
            logger.info('Successfully delete project {}'.format(project_name))
            return True

        except Exception as err:
            logger.error("Exception while deleting project in Ozone")
            logger.error(err.message)

    def update_ansible_variables(self, project_name, json_var):
        """
            Description: Upload input template for project in Ozone
            :param project_name - name for project(String)
            :param json_var - the file path of var json file(String)
            :return True/False
            """
        try:
            project = self.get_project_details_by_name(project_name)
            # Read input data from file
            with open(json_var, 'r') as f:
                project['components'] = {
                    'import_data': {
                        "hosts": [
                            {
                                "name": "localhost"
                            }
                        ],
                        "groups": [],
                        'vars': json.loads(f.read())
                    }
                }

            # Update input data to Ansible all group_var file
            url = 'https://{}/{}'.format(self._hostname, OZONE_UPDATE_VAR)
            response = self._session.post(url, json=project)
            logger.info(response.status_code)
            logger.info(response.content)
            if not response.ok:
                logger.error('Failed to update ansible variable files')
                return False
            logger.info('Successfully update ansible variable files for project {}'.format(project_name))

            # Update Project with new data (couchdb database)
            project_id = project['_id']
            url = 'https://{}/{}/{}'.format(self._hostname, OZONE_PROJECT_URL, project_id)
            self._session.put(url, json=project)
            logger.info(response.status_code)
            logger.info(response.content)
            if not response.ok:
                logger.error('Failed to update project {}'.format(project_name))
                return False
            logger.info('Successfully update project {}'.format(project_name))
            return True

        except Exception as err:
            logger.error("Exception while uploading input template in Ozone")
            logger.error(err.message)

    def validate_system_service(self):
        """
            Description: validate system service in ozone
            :return True/False
        """

        try:
            url = 'https://{}/{}'.format(self._hostname, OZONE_SYSTEM_URL)

            response = self._session.get(url)
            print response
            logger.info(response.status_code)
            logger.info(response.content)
            if not response.ok:
                logger.error('Failed to get system services in Ozone')
                return False
            logger.info('Successful to get system services in Ozone', )

            flag = True
            system_list = response.json()
            if not system_list['redis']['state']:
                logger.error('The servcie of Redis is not started.')
                flag = False
            logger.info('The servcie of Redis is started.')
            for system_list_service in system_list['forever']['data']:
                if 'running' not in system_list_service:
                    logger.error('The service {}  is not started'.format(system_list_service['id']))
                    flag = False
                else:
                    if not system_list_service['running']:
                        logger.error('The service {} is not running'.format(system_list_service['id']))
                        flag = False
                    logger.info('The service {} is true'.format(system_list_service['id']))
            if flag:
                logger.info('The service all started')
            return flag
        except Exception as err:
            logger.error("Exception while validate system services in Ozone")
            logger.error(err.message)

    def validate_system_agent(self):
        """
            Description: validate system agent in ozone
            :return True/False
            """
        try:
            url = 'https://{}/{}'.format(self._hostname, OZONE_SYSTEM_AGENT_URL)
            logger.info(url)

            response = self._session.get(url)
            logger.info(response.status_code)
            logger.info(response.content)
            if not response.ok:
                logger.error('Failed to get system services Agent')
                return False
            logger.info('Successful to get system services Agent')
            return True

        except Exception as err:
            logger.error("Exception while validate system services Agent in Ozone")
            logger.error(err.message)

    def get_project_details_by_name(self, project_name):
        """
            Description: Get project id by name in Ozone
            :param project_name - Ozone project name(String)
            :return Project id(String)
            """
        try:
            projectID = self.get_projectid_by_name(project_name)
            url = 'https://{0}/{1}/{2}'.format(self._hostname, OZONE_PROJECT_URL, projectID)

            response = self._session.get(url)
            logger.info(response.status_code)
            # logger.info(response.content)
            if not response.ok:
                logger.error('Failed to get project {}'.format(project_name))
                return False
            project = response.json()
            logger.info('Successfully find project {}'.format(project_name))
            return project

        except Exception as err:
            logger.error("Exception while getting project in Ozone")
            logger.error(err.message)
