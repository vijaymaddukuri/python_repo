import datetime

from TestExe.auc.auc import *
from TestExe.config.constants import *
from TestExe.config.constants import LOG_FILE_PATH


log.basicConfig(filename=LOG_FILE_PATH,level=log.DEBUG)
log.debug("*" * 60)
log.debug('Execution starts at {}'.format(datetime.datetime.now()))

#TESTCASE1 - Validate the results of diff type of integers, float values
TC1(TC1_INPUT_SCENARIO1)
TC1(TC1_INPUT_SCENARIO2)
TC1(TC1_INPUT_SCENARIO3)

# #TESTCASe2 -   Pass any random number (between 1-100) as a input and store the results.
# #          - Again pass the some other number as input and store the results
TC2(TC2_INPUT_VALUE1_SCENARIO1, TC2_INPUT_VALUE2_SCENARIO2)
TC2(TC2_INPUT_VALUE1_SCENARIO2, TC2_INPUT_VALUE2_SCENARIO2)
TC2(TC2_INPUT_VALUE1_SCENARIO3, TC2_INPUT_VALUE2_SCENARIO3)

# #TESTCASE3 - Pass string and special characters
TC3(TC3_INPUT_SCENARIO1)
TC3(TC3_INPUT_SCENARIO2)
TC3(TC3_INPUT_SCENARIO3)

