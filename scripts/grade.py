#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import argparse
import json
import csv
import subprocess

from scripts import path
from scripts import util


def load_config():
    grading_config_path = path.config_path / 'grading_config.json'
    with open(grading_config_path, 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['config']


def save_grades(csv_path, roster):
    headers = list(roster[next(iter(roster))].keys())

    with open(csv_path, 'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(roster.values())


def clean(config, homework_path):
    grader_test_files = config['grader_test_files'].split(',')
    grader_target = config['grader_target']
    student_target = config['student_target']

    util.del_file(homework_path / grader_target)
    util.del_file(homework_path / student_target)

    for file in grader_test_files:
        util.del_file(homework_path / file)


def copy_grader_files(config, test_path, homework_path):
    grader_test_files = config['grader_test_files'].split(',')

    for file in grader_test_files:
        success = util.copy_file(test_path / file, homework_path / file)

        if not success:
            return False

    return True


def grade_single(config, student_info, test_list, run_test, check_leak, show_details=True):
    homework_title = config['homework_title']
    last_name = student_info['last_name'].lower()
    first_name = student_info['first_name'].lower()
    repo_name = student_info['repo_name']
    folder_name = last_name + '_' + first_name + '/' + repo_name

    folder_path = path.homework_path / folder_name
    homework_path = folder_path / homework_title
    test_path = path.tests_path / homework_title

    grader_gcc_cmd = config['grader_compile_command']
    student_gcc_cmd = config['student_compile_command']
    total_grade = 0
    grading_comment = ""
    all_grades = {i_tid: 0 for i_tid in test_list}
    all_grades['total'] = 0

    print(first_name + " " + last_name + ":\n")

    # Copies all grader files.
    copy_success = copy_grader_files(config, test_path, homework_path)
    if not copy_success:
        print("ERROR: fail to copy the grader files.\n")
        clean(config, homework_path)
        return all_grades

    # Runs grader tests.
    if run_test:
        score_deducted = 0

        try:
            command = "cd %s " \
                      "&& %s " % (homework_path, grader_gcc_cmd)
            subprocess.call(command, shell=True)
        except subprocess.CalledProcessError:
            print("ERROR: compilation fails.\n")
            clean(config, homework_path)
            return all_grades

        for i_tid, i_value in test_list.items():
            try:
                command = str(homework_path / config['grader_target'])

                score_output = subprocess.check_output([command, i_tid], shell=False, timeout=config['timeout'])
                score_output = score_output.decode().splitlines()

                if score_output[-1].startswith("Score:"):
                    score_str = score_output[-1].split(':')[-1]
                    score = float(score_str)
                else:
                    score = 0

            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                score = 0

            if score == 0:
                score_deducted -= float(i_value['points'])
                grading_comment += "(-" + i_value['points'] + ") " + i_value['grading_comment'] + "\n"

            total_grade += score
            all_grades[i_tid] = score

            if show_details:
                print("Test case #%s: %f" % (i_tid, score))

        all_grades['total'] = total_grade
        full_points = sum(float(test_list[i]['points']) for i in test_list)
        print("Lost points: %.2f, total grade: %.2f / %.2f\n" % (score_deducted, total_grade, full_points))

        if show_details:
            print("Grading comments:")

            if score_deducted == 0:
                print("Good job!")
            else:
                print(grading_comment)

        print()

    # Runs the memory leak examinations.
    if check_leak:
        print("Memory leak examination: the student's unit tests\n")

        try:
            command = "cd %s " \
                      "&& %s " % (homework_path, student_gcc_cmd)
            subprocess.call(command, shell=True)

            exe_path = str(homework_path / config['student_target'])
            command = ["valgrind", exe_path, "> /dev/null"]
            subprocess.call(command, shell=False, stdout=subprocess.DEVNULL, timeout=config['timeout'])

        except subprocess.CalledProcessError as e:
            print("Memory leak examination error: %s\n" % e)
            pass

        print("\n")

        for i_tid in config['memory_leak_test_id']:
            print("Memory leak examination: grading test case #%d\n" % i_tid)

            try:
                command = "cd %s " \
                          "&& %s " % (homework_path, grader_gcc_cmd)
                subprocess.call(command, shell=True)

                exe_path = str(homework_path / config['grader_target'])
                command = ["valgrind", exe_path, str(i_tid), "> /dev/null"]
                subprocess.call(command, shell=False, stdout=subprocess.DEVNULL, timeout=config['timeout'])

            except subprocess.CalledProcessError as e:
                print("Memory leak examination error: %s\n" % e)
                pass

            print("\n")

    clean(config, homework_path)

    return all_grades


def grade(sid, run_test, check_leak):
    configs = load_config()

    for i_config in configs.values():
        roster = util.load_csv(path.rosters_path / i_config['roster_file'])
        homework_title = i_config['homework_title']
        test_list = util.load_csv(path.tests_path / homework_title / i_config['tests_list_file'])

        print("\n########## %s Grading ########## \n" % homework_title.capitalize())

        if sid is None:
            for i_student in roster.values():
                all_grades = grade_single(config=i_config, student_info=i_student, test_list=test_list,
                                          run_test=run_test, check_leak=False, show_details=False)
                i_student.update(all_grades)

            path.grades_path.mkdir(exist_ok=True)
            csv_name = i_config['homework_title'] + "_grades.csv"
            save_grades(path.grades_path / csv_name, roster=roster)

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
