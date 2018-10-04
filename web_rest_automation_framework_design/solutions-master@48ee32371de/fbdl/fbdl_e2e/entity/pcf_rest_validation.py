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

from .pcf_session import PCFSession
import urlparse


class PCFRestRequest(object):
    def __init__(self, username, password, api_url, uaa_url):
        self.session = PCFSession(username, password, api_url, uaa_url)

    def verify_space_deleted(self, org_name, space_name):
        if self.__get_space_url(org_name, space_name):
            return False
        else:
            return True

    def __get_space_url(self, org_name, space_name):
        _org_url = self.__get_org_url(org_name)
        if _org_url:
            _url = urlparse.urljoin(
                urlparse.urljoin(self.session.api_url, _org_url+'/'), 'spaces'
            )
            _response = self.session.get(_url)
            if _response.ok:
                _space_url = self.__get_resource_url(
                    space_name, _response.json()['resources'])
                return _space_url
            else:
                raise RuntimeError('Request spaces failed, response code: {}'
                                   .format(_response.status_code))
        else:
            raise ValueError('Org {} does not exist!'.format(org_name))

    def __get_org_url(self, org_name):
        _url = urlparse.urljoin(self.session.api_url, 'v2/organizations')
        _response = self.session.get(_url)
        if _response.ok:
            _org_url = self.__get_resource_url(
                org_name, _response.json()['resources'])
            return _org_url
        else:
            raise RuntimeError('Request Orgs failed, response code: {}'
                               .format(_response.status_code))

    def __get_resource_url(self, resource_name, resource_list):
        resource_url = None
        for resource in resource_list:
            if str(resource['entity']['name']) == str(resource_name):
                resource_url = str(resource['metadata']['url'])
                break
        return resource_url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
