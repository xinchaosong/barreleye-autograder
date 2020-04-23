# Barreleye Autograder

<img src="https://upload.wikimedia.org/wikipedia/commons/c/c0/Opisthoproctus_soleatus.png" width="200" alt="A barreleye fish">

A simple autograder for the computer science courses using GitHub to submit programming homework. It has been used for the following courses at Northeastern University:

- CS 3520: Programming in C++, Spring 2020
 
## Working Environment:

This tool is developed and tested with Python 3.7 on Debian 10. Using any other version of Python 3 or working on any other distribution of Linux should also work. Not check for macOS yet.

### Dependency:

- [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- Valgrind

## GitHub Repository Pulling Tool

### Preparation before running the script:

1. Make sure the current terminal can access to GitHub through SSH.
2. Modify the git configuration in *git_config.json* properly.
3. Fill all information of students into *roster.csv*.
4. Copy all following files into the folder used for further grading:

    - *repopull.py*
    - *repopull.sh*
    - *git_config.json*
    - *roster.csv*

### Pull all students' repositories:

Under the grading folder, use the following command to pull all repositories. If any repository is not pulled successfully, the program will try to re-clone it up to three time.

    ./repopull.sh

### Clone all students' repositories:

Under the grading folder, use the following command to clone all repositories. If any repository is not cloned successfully, the program will try to re-clone it up to three time. If the clone still fails, the program will prompt if the user wants to give up cloning and continue to process the next repository or exit the program. 

    ./repopull.sh -c

## Auto-Grading Tool with Tests

### Preparation before running the grading script:

1. Modify the grading configuration in *grading_config.json* properly.
2. Fill all information of students into *roster.csv*.
3. Make a proper test file compatible with the grader and students' homework
4. Check the folder structures of all students and modify anything wrong back to the standard way.
5. Copy all following files into the folder used for further grading:

	- *test\_list.csv*
	- *grading\_tests.c*
	- *grade.py*
	- *grade.sh*

### Grade a single student with both tests and memory-leak examinations:

Assume for grading a student who is in row 6 in the *roster.csv*, locate at the top level of the grading folder and run

    ./grade.sh 6

The detailed scores, grading comments, and Valgrind output will be shown on the screen.

### Grade a single student with tests only but not memory-leak examinations:

Assume for grading a student who is in row 6 in the *roster.csv*, locate at the top level of the grading folder and run

    ./grade.sh 6 -t

The detailed scores and grading comments will be shown on the screen.

### Grade a single student with memory-leak examinations only but not tests:

Assume for grading a student who is in row 6 in the *roster.csv*, locate at the top level of the grading folder and run

    ./grade.sh 6 -l

The Valgrind output will be shown on the screen.

### Grade all students together without memory-leak examinations:

Locating at the top level of the grading folder, run

    ./grade.sh

The total score for each student will be shown on the screen. The detailed scores will be recorded into *grades.csv*. No grading comments will be generated or shown.
