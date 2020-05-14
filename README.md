# Barreleye Autograder

<img src="barreleye-autograder.jpg" width="250px" alt="A barreleye fish">

## Introduction

This repository is a simple autograder for the computer science courses using GitHub to submit C/C++ programming homework. It can automatically clone/pull and grade the repositories of all students in a class using the instructor-made configurations and grading tests. All work can be done under the current folder structure of this repository so that the instructor does not need to copy or move any files manually.

This autograder has been used for the following courses at Northeastern University, Boston:

- CS 5006: Algorithms, Summer 2020
- CS 3520: Programming in C++, Spring 2020
 
## Environment Requirements

- Linux or macOS
- Python >= 3.7 (or 3.6 under CPython)
- Valgrind installed

## Preparation

### Download the Barreleye Autograder

	git clone git@github.com:xinchaosong/barreleye-autograder.git

### Before cloning/pulling the repository of students:

1. Make sure the current terminal can access to GitHub through SSH.
2. Under the folder **rosters**, fill all information of students into *roster.csv* (can be any name provided that it matches the git configuration in *git\_config.json*).
3. Under the folder **config**, modify the git configuration in *git\_config.json* properly. An example is shown below.

	    {
	      "git_config": {
	        "ssh_key_path": "~/.ssh/example_ssh",  // The full file path of the SSH key for GitHub
	        "roster_file": "example_roster.csv"    // The file name of the student roster
	      }
	    }

### Before running the grading script:

1. Under the folder **homework**, make sure all homework to be graded has been pulled/cloned there either by running this grader or manually copying. Check the folder structures of all students and modify anything wrong back to the standard way.
2. Under the folder **rosters**, fill all information of students into *roster.csv*.
3. Under the folder **grading-tests**, make a folder named by the homework title and put all test files such as *grading\_tests.c* and a corresponding test checklist file *test\_list.csv* that are compatible with the grader and students' homework.
5. Under the folder **config**, modify the grading configuration in *grading\_config.json* properly. An example is shown below.

		{
	      "config": {
	        // May setup multiple coonfigurations to run one by one
	        "0": {
	          "homework_title": "example-homework-c",          // The title of the homework to be graded
	          "roster_file": "example_roster.csv",             // The file name of the student roster
	          "tests_list_file": "example_test_list.csv",      // The file name of the test list
	          "grader_test_files": "example_grading_tests.c",  // All grading tests files used
	          "grader_compile_command": "gcc example_grading_tests.c homework.c -o grader",  
	                                                           // The command to compile the grading tests
	          "student_compile_command": "gcc main.c homework.c -o student",     
	                                                           // The command to compile the student' own tests
	          "grader_target": "grader",                       // The output target of the grading tests
	          "student_target": "student",                     // The output target of the student' own tests
	          "timeout": 10,                                   // Timeout in second
	          "memory_leak_test_id": [                         // The ids of grading tests to check memory leak
	            1,
	            4
	          ]
	        }
	      }
	    }

**Note:** *roster.csv*, *grading\_tests.c*, or *test\_list.csv* can be any name provided that the their name matches the grading configuration in *git\_config.json*

## Usage

If we use the example homework *example-homework-c* attached under the folder **homework** as an example, here are the available operations as follows.

### Clone/Pull all students' repositories:

    ./barreleye.sh -p

If any repository is not cloned successfully, the program will try to re-clone it **up to three times**. If the clone still fails for some reason, the program will prompt if the user wants to give up the current cloning and continue to process the next repository, or exit the program.

### Clone/Pull a specific student's repository:

For grading a student whose id is 1 in the *roster.csv*, use the following command to clone his/her repository. If the repository is not cloned successfully, the program will try to re-clone it **up to three times** before giving up.

    ./barreleye.sh -p -i 1

### Grade for all students together without memory-leak examinations:

    ./barreleye.sh

The total score for each student will be shown on the screen. The detailed scores will be recorded into *xxx\_grades.csv* under the folder **grades**. No grading comments will be generated or shown on the screen.

### Grade for a single student:

- Use the following command for grading a student whose id is 1 in the *roster.csv* with both tests and memory-leak examinations. The detailed scores, grading comments, and Valgrind output will be shown on the screen.

    	./barreleye.sh -i 1

- For grading the same student with tests only but not memory-leak examinations, add "-t" flag into the command as follows. The detailed scores and grading comments will be shown on the screen.

	    ./barreleye.sh -i 1 -t

- For grading the same student with memory-leak examinations only but not tests, add "-m" flag into the command as follows. The Valgrind output will be shown on the screen.

	    ./barreleye.sh -i 1 -m
