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


class DACCLIResponse(object):
    code = -1
    message = ''
    message_description = ''
    guid=''
    raw_message = ''
    workspace = ''
    name = ''
    category=''
    __guid_pattern = '.?([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}).?'

    def __init__(self, output_str):
        logger.info('Output:', False, True)
        logger.info(output_str, False, True)
        self.raw_message = output_str
        lines = [x for x in output_str.split('=') if x != '']
        lines = [x for x in output_str.split('\n') if x != '']
        if len(lines) == 3:
            fields = lines[2].split('|')
            if len(fields) !=3:
                logger.error('More than 3 columns message format is not supported yet!', False)
            else:
                self.code = fields[0].strip()
                self.message = fields[1].strip()
                self.message_description = fields[2].strip()
                import re
                match = re.search(self.__guid_pattern, fields[2].strip(), re.IGNORECASE)
                if match:
                    self.guid = match.group(1)
        else:
            logger.error('Not valid return message format!', False)
            logger.error(output_str, False)

    def copy(self, daccliobj):
        logger.info('copying the dac cli response object...', False, True)
        self.guid = daccliobj.guid
        self.workspace = daccliobj.workspace
        self.category = daccliobj.category
        self.name = daccliobj.name
