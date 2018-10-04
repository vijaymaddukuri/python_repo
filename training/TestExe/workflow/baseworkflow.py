from TestExe.config.constants import *

import training.TestExe.lib.utility as utils

input_value,output = utils.run_command(INPUT, EXE_FILE_PATH)

print input_value
print output