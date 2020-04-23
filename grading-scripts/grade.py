#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import json
import os
import subprocess
import argparse

import pandas as pd


def run_valgrind(cmd_str):
    subprocess.call(cmd_str, shell=True, timeout=5)


def load_config():
    with open("grading_config.json", 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['config']


def generate_compiling_cnd(config):
    gcc_cmd = config['command']
    source_files = config['source_files']
    grader_test_file = config['grader_test_file']
    student_test_file = config['student_test_file']
    grader_target = config['grader_target']
    student_target = config['student_target']

    grader_gcc_cmd = gcc_cmd + " " + grader_test_file + " " + source_files + " -o " + grader_target
    student_gcc_cmd = gcc_cmd + " " + student_test_file + " " + source_files + " -o " + student_target

    return grader_gcc_cmd, student_gcc_cmd


def grade(config, student_id, run_test, check_leak, show_details=True, to_csv=False):
    assignment_title = config['assignment_title']
    grader_gcc_cmd, student_gcc_cmd = generate_compiling_cnd(config)
    student_roster = pd.read_csv(os.path.join(os.path.dirname(__file__), config['student_roster']), index_col=0)
    test_list = pd.read_csv(os.path.join(os.path.dirname(__file__), config['tests_list']))
    last_name = str(student_roster.loc[student_id, 'last_name'])
    first_name = str(student_roster.loc[student_id, 'first_name'])
    repo_name = str(student_roster.loc[student_id, 'repo_name'])
    folder_name = last_name.lower() + '_' + first_name.lower() + '/' + repo_name
    assignment_path = folder_name + '/' + assignment_title
    grading_comment = ""

    print(first_name + " " + last_name + ":")

    if run_test:
        total = 0
        score_deducted = 0
        command = None

        try:
            command = "cp %s %s/%s" \
                      "&& cd %s " \
                      "&& %s " \
                      % (config['grader_test_file'], assignment_path, config['grader_test_file'],
                         assignment_path,
                         grader_gcc_cmd)
            subprocess.call(command, shell=True)

        except Exception:
            print("cp fails: %s" % command)
            return

        for j in range(test_list.shape[0]):
            try:
                command = "./%s/%s" % (assignment_path, config['grader_target'])

                score_output = subprocess.check_output([command, str(j + 1)], shell=False, timeout=5)
                score_output = score_output.decode().splitlines()

                if score_output[-1].startswith("Score:"):
                    score_str = score_output[-1].split(':')[-1]
                    score = float(score_str)
                else:
                    score = 0

            except Exception:
                score = 0

            if score == 0:
                score_deducted -= test_list.iloc[j, 2]
                grading_comment += "(-" + str(test_list.iloc[j, 2]) + ") " + str(test_list.iloc[j, 1]) + "\n"

            total += score

            if show_details:
                print("Test case #%d: %f" % (j + 1, score))

        full_points = sum(test_list.iloc[i, 2] for i in range(test_list.shape[0]))

        print("Lost points: %.2f, total grade: %.2f / %.2f\n" % (score_deducted, total, full_points))

        if show_details:
            print("Grading comments:")
            if score_deducted == 0:
                print("Good job!")
            else:
                print(grading_comment)

        print()

    if check_leak:
        if show_details:
            print("Memory leak check: the student's unit tests\n")

        try:
            command = "cd %s " \
                      "&& %s " \
                      "&& valgrind ./%s" % (assignment_path, student_gcc_cmd, config['student_target'])
            run_valgrind(command)

        except subprocess.CalledProcessError:
            pass

        if show_details:
            print("\n")

        for idx in range(len(config['memory_leak_test_id'])):

            if show_details:
                print("Memory leak check: grading test case #%d\n" %
                      config['memory_leak_test_id'][idx])

            try:
                command = "cd %s " \
                          "&& %s " \
                          "&& valgrind --log-fd=1 ./%s %d" \
                          % (assignment_path, grader_gcc_cmd, config['grader_target'],
                             config['memory_leak_test_id'][idx])
                run_valgrind(command)

            except subprocess.CalledProcessError:
                pass

            if show_details:
                print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-id', type=int)
    parser.add_argument('-t', action='store_false', help='only run tests but not memory leak check')
    parser.add_argument('-l', action='store_false', help='only run memory leak check but not tests')
    args = parser.parse_args()

    sid = int(args.i)
    m_run_test = args.l
    m_check_leak = args.t

    m_configs = load_config()

    for config_id in m_configs:
        if sid is None:
            num_students = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                    m_configs[config_id]['student_roster'])).shape[0]

            for s in range(num_students):
                grade(config=m_configs[config_id], student_id=s, run_test=m_run_test, check_leak=m_check_leak,
                      show_details=False)
        else:
            grade(config=m_configs[config_id], student_id=sid, run_test=m_run_test, check_leak=m_check_leak,
                  show_details=True)
