import requests
import json

MAX_CONNECTION_RETRIES=2
RETRY_ERRORS = [ "channel is not opened", "Connection aborted", "Connection refused", "Remote end closed connection without response" ]

class OzoneAPI:
        def __init__(self, OZONE_HOSTNAME, OZONE_PORT, OZONE_USERNAME, OZONE_PASSWORD):

            self.ozone_host = OZONE_HOSTNAME
            self.ozone_port = OZONE_PORT
            self.ozone_username = OZONE_USERNAME
            self.ozone_password = OZONE_PASSWORD
            self.access_token = None

        def format_url(self, api):
            api = api.replace("https://{0}:{1}/".format(self.ozone_host, self.ozone_port), "")
            return "https://{0}:{1}/{2}".format(self.ozone_host, self.ozone_port, api.strip("/"))

        # Submit HTTP Request
        def get_headers(self, content_type='application/json', xml=False, access_token=None):
            if xml:
                headers = {'Content-Type': content_type, 'ACCEPT': 'application/xml, application/octet-stream'}
            else:
                headers = {'Content-Type': content_type, 'ACCEPT': 'application/json, application/octet-stream'}

            if access_token:
                headers['authorization'] = 'Bearer ' + access_token
            elif self.access_token:
                headers['authorization'] = 'Bearer ' + self.access_token

            return headers

        # Submit HTTP Request
        def submit_http_request(self, http_method, uri, content_type='application/json', payload=None, xml=False,
                                trylogin=True,
                                files=None, access_token=None):
            retry = True
            retries = 0
            while retry:
                retries += 1
                if MAX_CONNECTION_RETRIES < retries:
                    raise Exception("Unable to connect to OzoneAPI. Max retries exceeded.")
                retry = False
                try:
                    return self.__submit_http_request(http_method, uri, content_type, payload, xml, trylogin, files,
                                                      access_token)
                except Exception as e:
                    # logger.warning("An error occurred while sending a request to vRealize Orchestrator. %s" % str(e))
                    for RETRY_ERROR in RETRY_ERRORS:
                        if RETRY_ERROR in str(e):
                            retry = True
                            break
                    if retry is False:
                        raise e

        def __submit_http_request(self, http_method, uri, content_type='application/json', payload=None, xml=False,
                                  trylogin=True,
                                  files=None, access_token=None):
            headers = self.get_headers(content_type, xml, access_token)

            url = self.format_url(uri)
            print("URL=" + url)
            # vro_auth = requests.auth.HTTPBasicAuth(admin_user, admin_password)
            session = requests.session()

            if http_method == 'GET':
                response = session.get(url, verify=False, headers=headers)
            elif http_method == 'POST':
                response = session.post(url, data=payload, verify=False, headers=headers, files=files)
            elif http_method == 'PUT':
                response = session.put(url, data=payload, headers=headers, verify=False)
            else:
                raise Exception("Unknown/Unsupported HTTP method: " + http_method)

            if response.status_code and response.status_code == requests.codes['ok'] or response.status_code == 202 or response.status_code == 201:
                # _logger.debug("Response: %s" % response.text)
                return response
            else:
                if response.status_code == 401:
                    # Try re login only once.
                    if trylogin:
                        # _logger.debug("Got an 401 error, trying to re-login")
                        self.login()
                        return self.submit_http_request(http_method, uri, content_type, payload, xml, False)
                    else:
                        # 401 response is html, so not parsing response
                        raise Exception(401, "Unauthorized")
                try:
                    error_json = json.loads(response.text)
                    raise Exception("%s: %s" % (str(response.status_code), error_json["details"]))
                except Exception as error_parsing_exception:
                    raise Exception("%s: %s" % (str(response.status_code), response.text))

        def login(self):
            response = self.submit_http_request('POST', 'auth/local',
                                                payload=json.dumps(
                                                    {'email': self.ozone_username, 'password': self.ozone_password}),
                                                trylogin=False)
            response_json = json.loads(response.text)
            print(response_json)
            self.access_token = response_json['token']

        def create_project(self, project_name, project_type):

            new_project = {
                "name": project_name,
                "type": project_type
            }

            try:
                response = self.submit_http_request('POST', 'api/projects',
                                                    payload=json.dumps(new_project))
                print(response.text)
                return response.json()
            except Exception as Excepion:
                print("Excepion - %s" % Excepion)

        def update_project(self, project_id, project):

            try:
                response = self.submit_http_request('PUT', 'api/projects/' + project_id,
                                                    payload=json.dumps(project))
                print(response.text)
                return response.json()
            except Exception as Excepion:
                print("Excepion - %s" % Excepion)
                raise
            

        def get_project(self, project_id):

            try:
                response = self.submit_http_request('GET', 'api/projects/' + project_id)
                print(response.text)
                return response.json()
            except Exception as Excepion:
                print("Excepion - %s" % Excepion)
                raise

        def update_ansible_variable_files(self, project):
            try:
                response = self.submit_http_request('POST', 'api/projects/update_ansible_variable_files', payload=json.dumps(project))
                print(response.text)
            except Exception as Excepion:
                print("Excepion - %s" % Excepion)
                raise

        def execute_ansible_job(self, ansible_job):
            try:
                response = self.submit_http_request('POST', 'api/ansible/execute', payload=json.dumps(ansible_job))
                print(response.text)
            except Exception as Excepion:
                print("Excepion - %s" % Excepion)
                raise

        def get_ansible_jobs(self, ref_id):
            try:
                response = self.submit_http_request('GET', 'api/ansible?' + 'refid=' + ref_id)
                print(response.text)
            except Exception as Excepion:
                print("Excepion - %s" % Excepion)
                raise


if __name__ == '__main__':
    ozoneApi = OzoneAPI('10.136.15.86', 443, 'service@ozone.com', 'Fehc@123')
    # Login to Ozone API
    ozoneApi.login()

    # Create New Project. Project name must be unique
    new_project = ozoneApi.create_project("Project12345678912345", "EHC4.1.1")

    # Get created project
    project = ozoneApi.get_project(new_project['id'])

    # Read input data from file
    f = open('input_data.json', 'r')

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
    ozoneApi.update_ansible_variable_files(project)

    # Update Project with new data (couchdb database)
    ozoneApi.update_project(new_project['id'], project)

    # Execute a playbook
    playbook_name = "Pre-Validation"
    ref_id = project['_id'] + "_" + playbook_name

    ansible_data = {
          'type': [ 'Pre-Validation' ],
          'refid': ref_id,  # Project ID + Playbook name
          'project': project,
            # use tags to specify task to run
            # NOTE: all tasks must be tagged and all tags to run must be specified here. Else task won't run.
          'tags': [ 'VAL - EPB-100-010 - Validate Input data'],
            # List all hosts to limit execution to. Note: Lists all hosts involved here.  This is list from inventory file.
          'limit_to_hosts': ['localhost'],
          'verbose': 'verbose',
          'check_mode': 'No_Check'}

    # Execute job. Asynchronous task. Returns immediately.
    ozoneApi.execute_ansible_job(ansible_data)

    # Get Job status. Run multiple time and poll until job is finished
    ozoneApi.get_ansible_jobs(ref_id)






