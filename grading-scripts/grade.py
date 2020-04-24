#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import argparse
import os
import json
import csv
import subprocess


def load_config():
    with open("grading_config.json", 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['config']


def load_csv(csv_path):
    data_sheet = {}

    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), csv_path)

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            data_sheet[row['id']] = row

    return data_sheet


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


def grade_single(config, student_info, test_list, run_test, check_leak, show_details=True, to_csv=False):
    assignment_title = config['assignment_title']
    grader_gcc_cmd, student_gcc_cmd = generate_compiling_cnd(config)
    last_name = student_info['last_name'].lower()
    first_name = student_info['first_name'].lower()
    repo_name = student_info['repo_name']
    folder_name = last_name + '_' + first_name + '/' + repo_name
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

        except subprocess.CalledProcessError:
            print("cp fails: %s" % command)
            return

        for tid, item in test_list.items():
            try:
                command = "./%s/%s" % (assignment_path, config['grader_target'])

                score_output = subprocess.check_output([command, tid], shell=False, timeout=30)
                score_output = score_output.decode().splitlines()

                if score_output[-1].startswith("Score:"):
                    score_str = score_output[-1].split(':')[-1]
                    score = float(score_str)
                else:
                    score = 0

            except subprocess.CalledProcessError:
                score = 0

            if score == 0:
                score_deducted -= item['points']
                grading_comment += "(-" + item['points'] + ") " + item['grading_comment'] + "\n"

            total += score

            if show_details:
                print("Test case #%s: %f" % (tid, score))

        full_points = sum(float(test_list[i]['points']) for i in test_list)

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
            print("Memory leak examination: the student's unit tests\n")

        try:
            command = "cd %s " \
                      "&& %s " % (assignment_path, student_gcc_cmd)
            subprocess.call(command, shell=True)

            exe_path = "./%s/%s" % (assignment_path, config['student_target'])
            subprocess.call(["valgrind", "--log-fd=1", exe_path], shell=False, timeout=30)

        except subprocess.CalledProcessError:
            print("Memory leak examination: ERROR\n")
            pass

        if show_details:
            print("\n")

        for idx in range(len(config['memory_leak_test_id'])):

            if show_details:
                print("Memory leak check: grading test case #%d\n" %
                      config['memory_leak_test_id'][idx])

            try:
                command = "cd %s " \
                          "&& %s " % (assignment_path, grader_gcc_cmd)
                subprocess.call(command, shell=True)

                exe_path = "./%s/%s" % (assignment_path, config['grader_target'])
                test_id = str(config['memory_leak_test_id'][idx])
                subprocess.call(["valgrind", "--log-fd=1", exe_path, test_id], shell=False, timeout=30)

            except subprocess.CalledProcessError:
                print("Memory leak examination: ERROR\n")
                pass

            if show_details:
                print("\n")


def grade(sid, run_test, check_leak):
    configs = load_config()

    for i_config in configs.values():
        roster = load_csv(i_config['student_roster'])
        test_list = load_csv(i_config['tests_list'])

        if sid is None:
            for i_student in roster.values():
                grade_single(config=i_config, student_info=i_student, test_list=test_list,
                             run_test=run_test, check_leak=check_leak, show_details=False)
        else:
            grade_single(config=i_config, student_info=roster[sid], test_list=test_list,
                         run_test=run_test, check_leak=check_leak, show_details=True)


if __name__ == "__main__":
    m_parser = argparse.ArgumentParser()
    m_parser.add_argument('-i', '-id')
    m_parser.add_argument('-t', action='store_false', help='only run tests but not memory leak check')
    m_parser.add_argument('-m', action='store_false', help='only run memory leak check but not tests')
    m_args = m_parser.parse_args()

    grade(sid=m_args.i, run_test=m_args.m, check_leak=m_args.t)
