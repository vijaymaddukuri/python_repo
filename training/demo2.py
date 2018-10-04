import os.path
import re

from subprocess import check_output
os.getcwd()
os.chdir(r'V:\Learning\RideCO\QA_screener_test')


your_exe_file_address = "testme.exe"
input_value = "10"

response = check_output([your_exe_file_address, input_value])
print(type(response))

input_pattern = 'input:\s(\d+)'
output_patterh = 'output:\s(\d+)'
m= re.search(input_pattern, str(response), re.IGNORECASE)
input = m.group(1)
m= re.search(output_patterh, str(response), re.IGNORECASE)
output = m.group(1)
print(input)
print(output)
