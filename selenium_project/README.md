Steps to run :
1. Put both the files(new_project_automation.tar and test_runner.sh) in a directory.#Both the files should be in same directory
2. chmod +x test_runner.sh #Give permissions 
3. ./test_runner.sh #Run the shell script, it might prompt you for sudo permissions.

NOTE : 
1. The script currently supports CentOS and Ubuntu, to run on any other Linux flavor :
   Manually Install "pip"  and then follow the "Steps to run" above.
2. It runs tests on Firefox, because Firefox comes "out of the box" in Linux OS.
3. It requires Python 2.7.x to be installed on the machines, which also comes "out of the box" in Linux OS.

