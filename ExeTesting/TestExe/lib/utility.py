import logging as log
import re
import subprocess
import sys

from os import path


def run_command(input_number, app_path=''):
    """This module will execute the Testme.exe file with integer input and
    returns the input and output values in string format
    :param input_number: Integer Input to the testme.exe (ex: 10)
    :param app_path: Path of the testme.exe file
    :return: Returns Input and output strings (10, 2983557137299388795107192986413907782003447359461)
    :except: Input, OS, Subprocess, Regex errors
    """
    output_dict = {}
    # Validate the testme app exists or not
    result= path.exists(app_path)
    if not result:
        log.debug("Please pass the valid path for the testme application {}".format(app_path))
        return output_dict
    try:
        # Validate the input is integer or not.
        int(input_number)
    except ValueError:
        log.debug("TypeError: Please pass the integer input")
    try:
        log.info('Executing the Testme Application with the command '
                  'testme {}'.format(input_number))
        process = subprocess.Popen([app_path, str(input_number)], stdout=subprocess.PIPE)
        result = process.communicate()
        log.info('Successfully executed the command '
                  'testme {}'.format(input_number))
        if process.returncode:
            log.debug('Unable to execute the command')
            raise RuntimeError('Unable to execute the command')
        log.info('Execution log: \n{}'.format(str(result[0])))
    except OSError as e:
        log.debug("OSError > ", e.errno)
        log.debug("OSError > ", e.strerror)
        log.debug("OSError > ", e.filename)
    except subprocess.CalledProcessError as caller:
        log.debug('Process exits with a non-zero exit code {}'.format(caller))
    try:
        if result:
            # Using regular expressions get the out values
            log.debug('Using regular expression getting the output value')
            output_value = re.search('output:\s(\d+)', str(result[0]), re.I)
            if output_value:
                output_dict['output'] = output_value.group(1)
    except re.error as regex:
        log.debug('Regular expression error {}'.format(regex))
    except KeyError:
        log.debug('Unable to get the output value')
    except:
        log.debug("Unexpected error: {}".format(sys.exc_info()[0]))
    return output_dict
