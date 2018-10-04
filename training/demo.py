from subprocess import Popen, check_output, check_call, PIPE, call


get_input = input("What Should I do?")

if get_input.strip().lower() == "run":

    your_exe_file_address = r'"V:\Learning\RideCO\QA_screener_test\testme.exe"' # example
    your_module_address = r'"C:\Users\you\Desktop\test.m"' # example
    your_command = "10"
    process = Popen([your_exe_file_address, your_command], stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()

    # < Other Ways >
    # process = check_output([your_exe_file_address, your_command, your_module_address])
    # process = check_call([your_exe_file_address, your_command, your_module_address], shell=True)
    # process = call([your_exe_file_address, your_command, your_module_address], stdout=PIPE, stderr=PIPE, shell=True)

    print(stdout, stderr)

else:
    print("Invalid Input")