import logging as log
import TestExe.lib.utility as utils

from TestExe.config.constants import EXE_FILE_PATH


def compare_the_values(dict1, dict2):
    """
    Compare the output of two differ dict values
    :param dict1: Dict1
    :param dict2: Dict2
    :return: Boolean True or false
    """
    return True if dict1['output'] == dict2['output'] else False

def TC1(input):
    """
    Validate the results of diff type of integers, float values
    :param input: integer
    """
    log.debug("Test case 1 execution started")
    result= utils.run_command(input, EXE_FILE_PATH)
    if (int(result['output'])):
        log.debug("Test case 1 executed successfully")
    else:
        log.debug("Test case 1 failed due to invalid output")

def TC2(input1, input2):
    """
    -	Pass any random number (between 1-100) as a input and store the results.
    -	Again pass the some other number as input and store the results
    :param input1: integer
    :param input2: integer
    :return: If both the outputs are same True, else return False
    """
    log.debug("Test case 2 execution started")
    result1 = utils.run_command(input1, EXE_FILE_PATH)
    result2 = utils.run_command(input2, EXE_FILE_PATH)
    result=compare_the_values(result1,result2)
    if result:
        log.debug("Test case 2 executed successfully")
    else:
        log.debug("Test case 2 failed due to different "
                  "outputs = output1:{} output2:{}".format(result1['output'],result2['output']))

def TC3(input):
    """
    #TESTCASE3 - Pass string and special characters
    :param input: string
    """
    log.debug("Test case 3 execution started")
    try:
        # Validate the input is integer or not.
        int(input)
        result = utils.run_command(input, EXE_FILE_PATH)
        if (int(result['output'])):
            log.debug("Test case 3 executed successfully")
        else:
            log.debug("Test case 3 failed due to invalid output")
    except ValueError:
        log.debug("Test case 3 execution failed due to invalid input string {},"
                  " please pass integer as input".format(input))