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
from robot.api import logger
import requests
import time


class DACRESTQuery(object):
    __end_point = ''

    def __init__(self, end_point):
        self.__end_point = end_point

    def run(self):
        logger.debug('query on {} '.format(self.__end_point), True)
        default_timeout = 60
        timer = 0
        while timer<default_timeout:
            timer += 1
            response = requests.get(self.__end_point)
            if response.status_code == 200:
                try:
                    status = response.json()['body']['processStatus'][0]['processStatus']
                except IndexError:
                    logger.error('Invalid format of the returned message!', True)
                    return
                if status == 'successful':
                    logger.debug('Job finishes successfully!', True)
                    return
                elif status == 'failed':
                    #logger.error('job failed due to reason: {}'.format(self._get_key_from_dict(response.json(),'processResultDetails')), True)
                    raise AssertionError('submit template job failed')
                else:
                    time.sleep(1)
                    continue
            else:
                logger.error('Bad Return code for the query call. {}:{} '.format(response.status_code, response.reason))
                raise AssertionError('Bad Return code for the query call. {} '.format(response.status_code))

    def get_assets_name_list(self):
        logger.debug('query on {} '.format(self.__end_point), True)
        response = requests.get(self.__end_point)
        _name_list = []
        if response.status_code == 200:
            try:
                assets_count = response.json()['body']['totalItemCount']
            except KeyError:
                logger.error('Invalid format of the returned message!', True)
                return None
            if int(assets_count) > 0:
                try:
                    _assets_list = response.json()['body']['list']
                except KeyError:
                    logger.error('Invalid format of the returned message!', True)
                    return None
                for item in _assets_list:
                    try:
                        _name_list.append(item['AssetVisibleName'])
                    except KeyError:
                        logger.error('Invalid format of the returned message!', True)
                        return None
                return _name_list
            else:
                return 0
        else:
            logger.error('query on {url} failed, status code was {status_code}'
                         .format(url=self.__end_point, status_code=response.status_code), True)
            return None
