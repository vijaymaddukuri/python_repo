# word_puzzle

####
Given a size of  board, this Python program prints out all of the words (and their points)
contained within the board. Valid words are given in the words.txt file.
Finally, the Python program prints all valid words which can be theoretically obtain.


### Software Requirements

    Python 3 or above

### Build the project

1. Execute build.sh from project root - to generate build artifacts in the dist directory

        $ ./build.sh

### Create Python virtual environment

        $ virtualenv <name-of-folder> -p python --never-download [If internet is not there, command will not
                                                                  try to download packages from internet]

### Activate virtual environment

        $ source <path-to-folder>/bin/activate

### Install requirements

        $ pip install -r requirements/requirements.txt

### Run Flake8 before commit (run on the root of the project)

        $ flake8 .

### Run the unit testcases (run on the root of the project)

        $ python -m "nose" --with-coverage --cover-package=.

### Command to run the Project

    Go to the directory workflow (wordpuzzle/workflow) and execute below python command with optional parameters

    Command:

        python puzzle_solver.py -s <borad size> -p <word file path>

    Command line Arguments:

        '-s' or --size: Board size (default is 4)
        '-p' or  --filepath: Path of words.txt file (default is <root_dir>/conf/words.txt)

    Command example:

        python puzzle_solver.py -s 15 -p C://Users//madduv//Desktop//words.txt

                                or
        python puzzle_solver.py


### Deactivate virtual environment

        $ deactivate

### Result

    Results will be stored in log file (at the root of the project)

        log file name: word_puzzle_<time_stamp>.log
