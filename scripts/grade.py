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


def grade(sid, check_tests, check_leak):
    configs = load_config()

    for i_cdx, i_config in configs.items():
        roster = util.load_csv(path.rosters_path / i_config['roster_file'])
        homework_title = i_config['homework_title']
        tests_path = path.tests_path / i_config['test_files_path']
        test_list = util.load_csv(tests_path / i_config['tests_list_file'])

        print("\n########## %s %s Grading ########## \n" % (homework_title.capitalize(), i_cdx.capitalize()))

        if sid is None:
            for i_student in roster.values():
                all_grades = grade_single(config_id=i_cdx, config=i_config, student_info=i_student,
                                          test_list=test_list, check_tests=check_tests, check_leak=check_leak,
                                          show_details=False)
                i_student.update(all_grades)

            path.grades_path.mkdir(exist_ok=True)
            csv_name = i_config['homework_title'] + "_" + i_cdx + "_grades.csv"
            save_grades(path.grades_path / csv_name, roster=roster)

        else:
            grade_single(config_id=i_cdx, config=i_config, student_info=roster[sid], test_list=test_list,
                         check_tests=check_tests, check_leak=check_leak, show_details=True)


def load_config():
    grading_config_path = path.config_path / 'grading_config.json'
    with open(grading_config_path, 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['config']


def grade_single(config_id, config, student_info, test_list, check_tests, check_leak, show_details=True):
    homework_title = config['homework_title']
    last_name = student_info['last_name']
    first_name = student_info['first_name']
    repo_name = student_info['repo_name']
    folder_name = last_name.lower() + '_' + first_name.lower() + '/' + repo_name

    folder_path = path.homework_path / folder_name
    homework_path = folder_path / homework_title
    tests_path = path.tests_path / config['test_files_path']
    log_path = homework_path / ("grading_log_%s.txt" % config_id.lower())

    grader_gcc_cmd = config['grader_compile_command']
    student_gcc_cmd = config['student_compile_command']

    all_grades = {i_tid: 0 for i_tid in test_list}
    all_grades['total'] = 0

    logger = util.GradingLogger()
    logger.log("Grading Result:\n")

    print(first_name + " " + last_name + ":\n")

    # Copies all grader files.
    copy_success = copy_grader_files(config, tests_path, homework_path)
    if not copy_success:
        err_msg = "ERROR: fail to copy the grader files.\n"
        logger.log(err_msg)
        print(err_msg)

        logger.save_log(log_path)
        clean(config, homework_path)

        return all_grades

    # Runs grader tests.
    if check_tests:
        all_grades = run_grading_tests(homework_path=homework_path,
                                       grader_gcc_cmd=grader_gcc_cmd,
                                       grader_target=config['grader_target'],
                                       test_list=test_list,
                                       all_grades=all_grades,
                                       logger=logger,
                                       timeout=config['timeout'],
                                       show_details=show_details)

    # Runs the memory leak examinations.
    if check_leak:
        run_memory_exam(homework_path=homework_path,
                        student_gcc_cmd=student_gcc_cmd,
                        student_target=config['student_target'],
                        grader_gcc_cmd=grader_gcc_cmd,
                        grader_target=config['grader_target'],
                        memory_leak_test_ids=config['memory_leak_test_id'],
                        logger=logger,
                        timeout=config['timeout'],
                        show_details=show_details)

    logger.save_log(log_path)
    clean(config, homework_path)

    return all_grades


def copy_grader_files(config, test_path, homework_path):
    grader_test_files = config['grader_test_files'].split(',')

    for file in grader_test_files:
        success = util.copy_file(test_path / file, homework_path / file)

        if not success:
            return False

    return True


def run_grading_tests(homework_path, grader_gcc_cmd, grader_target, test_list, all_grades, logger, timeout,
                      show_details=False):
    stdout = None if show_details else subprocess.DEVNULL
    stderr = None if show_details else subprocess.DEVNULL

    total_grade = 0
    score_deducted = 0
    grading_comment = ""

    logger.log("Grading unit tests:\n", to_stdout=show_details)

    # Compilation
    try:
        compile_code(homework_path, grader_gcc_cmd, stdout=stdout, stderr=stderr)
    except Exception:
        err_msg = "ERROR: compilation fails during running grading unit tests.\n"
        logger.log(err_msg)
        print(err_msg)

        return all_grades

    # Runs all tests
    for i_tid, i_value in test_list.items():
        try:
            # The heap consistency checking level is set to 2 so that any test causing memory
            # heap corruption will simply abort without outputting too many error messages.
            command = "export MALLOC_CHECK_=2 && " \
                      "%s %s" % (str(homework_path / grader_target), i_tid)
            score_output = subprocess.check_output(command, stderr=stderr, shell=True,
                                                   timeout=timeout).decode().splitlines()

            if score_output[-1].startswith("Score:"):
                score_str = score_output[-1].split(':')[-1]
                score = float(score_str)
            else:
                score = 0

        except Exception as e:
            score = 0

        if score == 0:
            score_deducted -= float(i_value['points'])
            grading_comment += "(-" + i_value['points'] + ") " + i_value['grading_comment'] + "\n"

        total_grade += score
        all_grades[i_tid] = score

        logger.log("Test case #%s: %f" % (i_tid, score), to_stdout=show_details)

    # Summarization
    all_grades['total'] = total_grade
    full_points = sum(float(test_list[i]['points']) for i in test_list)
    summary = "Lost points: %.2f, total grade: %.2f / %.2f\n" % (score_deducted, total_grade, full_points)
    logger.log(summary, to_stdout=True)

    if score_deducted == 0:
        grading_comment = "Good job!"

    logger.log("Grading comments:", to_stdout=show_details)
    logger.log(grading_comment + "\n", to_stdout=show_details)

    return all_grades


def compile_code(homework_path, grader_gcc_cmd, stdout=None, stderr=None):
    command = "cd %s " \
              "&& %s " % (homework_path, grader_gcc_cmd)
    subprocess.run(command, stdout=stdout, stderr=stderr, shell=True, check=True)


def run_memory_exam(homework_path, student_gcc_cmd, student_target, grader_gcc_cmd, grader_target,
                    memory_leak_test_ids, logger, timeout, show_details=False):
    stdout = None if show_details else subprocess.DEVNULL
    stderr = None if show_details else subprocess.DEVNULL

    # Memory leak examination: the student's unit tests
    logger.log("Memory leak examination: the student's unit tests\n", to_stdout=show_details)

    try:
        # Compilation
        compile_code(homework_path, student_gcc_cmd, stdout=stdout, stderr=stderr)

        # Runs Valgrind
        try:
            result = runs_valgrind(str(homework_path / student_target), timeout=timeout)
        except Exception as e:
            result = "Memory leak examination error: %s\n" % e

    except Exception:
        result = "ERROR: compilation fails during memory leak examination. \n"

    logger.log(result + "\n", to_stdout=show_details)

    # Memory leak examination: grading tests
    for i_tid in memory_leak_test_ids:
        logger.log("Memory leak examination: grading test case #%d\n" % i_tid, to_stdout=show_details)

        try:
            # Compilation
            compile_code(homework_path, grader_gcc_cmd, stdout=stdout, stderr=stderr)

            # Runs Valgrind
            try:
                result = runs_valgrind(str(homework_path / grader_target), str(i_tid), timeout=timeout)
            except Exception as e:
                result = "Memory leak examination error: %s\n" % e

        except Exception:
            result = "ERROR: compilation fails during memory leak examination. \n"

        logger.log(result + "\n", to_stdout=show_details)


def runs_valgrind(*args, timeout=10):
    command = ["valgrind"] + list(args)

    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=timeout,
                          check=True).stderr.decode()


def clean(config, homework_path):
    grader_test_files = config['grader_test_files'].split(',')
    grader_target = config['grader_target']
    student_target = config['student_target']

    util.del_file(homework_path / grader_target)
    util.del_file(homework_path / student_target)

    for file in grader_test_files:
        util.del_file(homework_path / file)


def save_grades(csv_path, roster):
    headers = list(roster[next(iter(roster))].keys())

    with open(csv_path, 'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(roster.values())


if __name__ == "__main__":
    m_parser = argparse.ArgumentParser()
    m_parser.add_argument('-i', '-id')
    m_parser.add_argument('-t', action='store_false', help='only run tests but not memory leak check')
    m_parser.add_argument('-m', action='store_false', help='only run memory leak check but not tests')
    m_args = m_parser.parse_args()

    grade(sid=m_args.i, check_tests=m_args.m, check_leak=m_args.t)
