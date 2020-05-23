#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 25, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import argparse
import os
import sys
from pathlib import Path

if __name__ == '__main__':
    m_parser = argparse.ArgumentParser()
    m_parser.add_argument('-i', '-id')
    m_parser.add_argument('-p', '-pull', action='store_true', help='pull the repository(ies)')
    m_parser.add_argument('-t', action='store_false', help='only run tests but not memory leak check')
    m_parser.add_argument('-m', action='store_false', help='only run memory leak check but not tests')
    m_args = m_parser.parse_args()

    # Guarantee the working paths are correct
    os.chdir(sys.path[0])
    sys.path.append(str(Path.cwd().parent))
    from scripts.pull import pull
    from scripts.grade import grade

    if m_args.p:
        pull(sid=m_args.i)
    else:
        grade(sid=m_args.i, check_tests=m_args.m, check_leak=m_args.t)
