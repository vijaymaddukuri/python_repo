import subprocess
import re
import logging as log
import sys


def run_command(input_number, path='testme'):
    '''This module will execute the Testme.exe file and
    returns the input and output values in string format
    :param input_number: Integer Input to the testme.exe (ex: 10)
    :param path: Path of the testme.exe file
    :return: Returns Input and output strings (10, 2983557137299388795107192986413907782003447359461)
    '''
    try:
        p = subprocess.Popen([path, str(input_number)], stdout=subprocess.PIPE)
        result = p.communicate()
        if result[0]:
            input_value = re.search('input: (.*)', result[0], re.I)
            output_value = re.search('output: (.*)', result[0], re.I)
            if input_value and output_value :
                return input_value.group(1), output_value.group(1)

    except OSError as e:
        log.debug("OSError > ", e.errno)
        log.debug("OSError > ", e.strerror)
        log.debug("OSError > ", e.filename)
    except:
        log.debug("Unexpected error:", sys.exc_info()[0])