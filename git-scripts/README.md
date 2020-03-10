## XSVM Autograder - Git Script

### Working Environment:

This tool is developed and tested with Python 3.7 on Debian 10. Using any other version of Python 3 or working on any other distribution of Linux should also work. Not check for macOS yet.

### Dependency:

- [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)

### Preparation before running the script:

1. Make sure the current terminal can access to GitHub through SSH.
2. Modify the configuration in `git_config.json` properly.
3. Fill all information of students into `roster.csv`.
4. Copy all following files into the folder used for further grading.

    - `repopull.py`
    - `repopull.sh`
    - `git_config.json`
    - `roster.csv`

### Pull all students' repositories:

Under the grading folder, use the following command to pull all repositories. If any repository is not pulled successfully, the program will try to re-clone it up to three time.

    ./repopull.sh

### Clone all students' repositories:

Under the grading folder, use the following command to clone all repositories. If any repository is not cloned successfully, the program will try to re-clone it up to three time. If the clone still fails, the program will prompt if the user wants to give up cloning and continue to process the next repository or exit the program. 

    ./repopull.sh -c
