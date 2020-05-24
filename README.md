# Barreleye Autograder

<img src="barreleye-autograder.jpg" width="250px" alt="A barreleye fish">

## Introduction

This repository is a simple autograder for the computer science courses using GitHub to submit C/C++ programming homework. It can automatically clone/pull and grade the repositories of all students in a class using the instructor-made configurations and grading tests. All work can be done under the current directory structure of this repository so that the instructor does not need to copy or move any files manually.

This autograder has been used for the following courses at Northeastern University, Boston:

- CS 5006: Algorithms, Summer 2020
- CS 3520: Programming in C++, Spring 2020

## Features

- Downloading all student's repositories automatically
- Running the instructor-made tests for all students automatically
- Batch grading and automatically generating grading sheet and grading reports
- Able to handle tests crash and timeout issues
- Customized configurations to fit different needs
 
## Environment Requirements

- Linux or macOS
- Python >= 3.7 (or 3.6 under CPython)
- Valgrind installed

## Preparation

### Download the Barreleye Autograder

	git clone https://github.com/xinchaosong/barreleye-autograder.git

### Before cloning/pulling the repository of students:

1. Make sure the current terminal can access to GitHub through SSH using a SSH key with no passphrase. If you are not familar with connecting to GitHub with SSH, please follow [this tutorial](https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) from GitHub. 
2. Under the directory **rosters**, fill all information of students into *roster.csv* (can be any name provided that it matches the git configuration in *git\_config.json*).
3. Under the directory **config**, modify the git configuration in *git\_config.json* properly. An example is shown below.

	    {
	      "git_config": {
	        "ssh_key_path": "~/.ssh/example_ssh",  // The full file path of the SSH key for GitHub
	        "roster_file": "example_roster.csv"    // The file name of the student roster
	      }
	    }

### Before running the grading script:

1. Under the directory **homework**, make sure all homework to be graded has been pulled/cloned there either by running this grader or manually copying. Check the directory structures of all students and modify anything wrong back to the standard way.
2. Under the directory **rosters**, fill all information of students into *roster.csv*.
3. Under the directory **grading-tests**, make a folder named by the homework title and put all test files such as *grading\_tests.c* and a corresponding test checklist file *test\_list.csv* that are compatible with the grader and students' homework.
5. Under the directory **config**, modify the grading configuration in *grading\_config.json* properly. An example is shown below.

		{
	      "config": {
	        // May setup multiple coonfigurations to run one by one
	        "All": {
	          "homework_title": "example-homework-c",          // The title of the homework to be graded
	          "roster_file": "example_roster.csv",             // The file name of the student roster
              "test_files_path": "example-homework-c",         // The relative path to the folder that contains
                                                               // all tests under the grading-tests directory
	          "tests_list_file": "example_tests_list.csv",     // The file name of the test list
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

If we use the example homework *example-homework-c* attached under the directory **homework** as an example, here are the available operations as follows.

### Clone/Pull all students' repositories:

    ./barreleye.sh -p

If any repository is not cloned successfully, the program will try to re-clone it **up to three times**. If the clone still fails for some reason, the program will prompt if the user wants to give up the current cloning and continue to process the next repository, or exit the program.

### Clone/Pull a specific student's repository:

For grading a student whose id is 1 in the *roster.csv*, use the following command to clone his/her repository. If the repository is not cloned successfully, the program will try to re-clone it **up to three times** before giving up.

    ./barreleye.sh -p -i 1

### Grade for all students together without memory-leak examinations:

    ./barreleye.sh

The total score for each student will be shown on the screen. The detailed scores will be recorded into *xxx\_grades.csv* under the directory **grades**. No grading comments will be generated or shown on the screen. A grading report recording all details will be generate for each student under the student's directory for the given homework graded.

### Grade for a single student:

- Use the following command for grading a student whose id is 1 in the *roster.csv* with both tests and memory-leak examinations. The detailed scores, grading comments, and Valgrind output will be shown on the screen. A corresponding grading report will be generate under the student's directory for the given homework graded.

    	./barreleye.sh -i 1

- For grading the same student with tests only but not memory-leak examinations, add "-t" flag into the command as follows. The detailed scores and grading comments will be shown on the screen. A corresponding grading report will be generate under the student's directory for the given homework graded.

	    ./barreleye.sh -i 1 -t

- For grading the same student with memory-leak examinations only but not tests, add "-m" flag into the command as follows. The Valgrind output will be shown on the screen. A corresponding grading report will be generate under the student's directory for the given homework graded.

	    ./barreleye.sh -i 1 -m
