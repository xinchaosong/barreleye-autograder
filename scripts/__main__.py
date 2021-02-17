#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 25, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import argparse
import os
import sys
from pathlib import Path

if __name__ == '__main__':
    try:
        m_parser = argparse.ArgumentParser()
        m_subparsers = m_parser.add_subparsers(help='sub-command help')

        # Pulling
        m_parser_pull = m_subparsers.add_parser('pull', help='pull the repository(ies)')
        m_parser_pull.add_argument('-i', '--id', help='process a particular assignment with the given student id')
        m_parser_pull.add_argument('--https', action='store_true', help='pull the repository(ies) using https urls')

        # Grading
        m_parser_grade = m_subparsers.add_parser('grade', help='grade the repository(ies)')
        m_parser_grade.add_argument('-i', '--id', help='process a particular assignment with the given student id')
        m_parser_grade.add_argument('-t', action='store_false', help='only run tests but not memory leak check')
        m_parser_grade.add_argument('-m', action='store_false', help='only run memory leak check but not tests')

        m_args = m_parser.parse_args()

        # Guarantee the working paths are correct
        os.chdir(sys.path[0])
        sys.path.append(str(Path.cwd().parent))
        from scripts.pull import pull
        from scripts.grade import grade

        if 'https' in m_args:
            pull(sid=m_args.id, https=m_args.https)
        else:
            grade(sid=m_args.id, check_tests=m_args.m, check_leak=m_args.t)

    except (KeyboardInterrupt, SystemExit):
        print()
