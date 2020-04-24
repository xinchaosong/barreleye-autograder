# Barreleye Autograder

<img src="https://upload.wikimedia.org/wikipedia/commons/c/c0/Opisthoproctus_soleatus.png" width="200" alt="A barreleye fish">

A simple autograder for the computer science courses using GitHub to submit C/C++ programming homework. It has been used for the following courses at Northeastern University, Boston:

- CS 3520: Programming in C++, Spring 2020
 
## Environment Requirements:

- Linux or macOS
- Python >= 3.6
- [Valgrind](http://valgrind.org/downloads/current.html) installed

## GitHub Repository Pulling Tool

### Preparation before running the script:

1. Make sure the current terminal can access to GitHub through SSH.
2. Fill all information of students into *roster.csv* (can be any name provided that it matches the git configuration in *git_config.json*).
3. Modify the git configuration in *git_config.json* properly.
4. Copy all following files into a folder used for further grading:

    - *roster.csv*
    - *git_config.json*
    - *repopull.py*
    - *repopull.sh*

### Usage

If we use *example-assignment-c* attached as an example, here are the available operations as follows.

#### Pull all students' repositories:

Under the grading folder, use the following command to pull all repositories. If any repository is not pulled successfully, the program will try to re-clone it up to three times.

    ./repopull.sh

#### Clone all students' repositories:

Under the grading folder, use the following command to clone all repositories. If any repository is not cloned successfully, the program will try to re-clone it up to three times. If the clone still fails, the program will prompt if the user wants to give up cloning and continue to process the next repository or exit the program. 

    ./repopull.sh -c

## Auto-Grading Tool with Tests

### Preparation before running the grading script:

1. Fill all information of students into *roster.csv*.
2. Make a proper test file *grading\_tests.c* compatible with the grader and students' homework.
3. Make a corresponding test checklist file *test\_list.csv* compatible with the grader and students' homework.
1. Modify the grading configuration in *grading_config.json* properly.
4. Check the folder structures of all students and modify anything wrong back to the standard way.
5. Copy all following files into a folder used for further grading:

	- *roster.csv*
	- *grading\_tests.c*
	- *test\_list.csv*
	- *grade.sh*
	- *grade.py*

(*roster.csv*, *grading\_tests.c*, or *test_list.csv* can be any name provided that the new name matches the grading configuration in *git_config.json*)

### Usage

If we use *example-assignment-c* attached as an example, here are the available operations as follows.

#### Grade for all students together without memory-leak examinations:

Locating at the top level of the grading folder, run

    ./grade.sh

The total score for each student will be shown on the screen. The detailed scores will be recorded into *grades.csv*. No grading comments will be generated or shown.

#### Grade for a single student with both tests and memory-leak examinations:

For grading a student whose id is 6 in the *roster.csv*, locate at the top level of the grading folder and run

    ./grade.sh 6

The detailed scores, grading comments, and Valgrind output will be shown on the screen.

#### Grade for a single student with tests only but not memory-leak examinations:

For grading a student whose id is 6 in the *roster.csv*, locate at the top level of the grading folder and run

    ./grade.sh 6 -t

The detailed scores and grading comments will be shown on the screen.

#### Grade for a single student with memory-leak examinations only but not tests:

For grading a student whose id is 6 in the *roster.csv*, locate at the top level of the grading folder and run

    ./grade.sh 6 -m

The Valgrind output will be shown on the screen.
