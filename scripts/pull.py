#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import argparse
import json

from scripts import git_tools
from scripts import path
from scripts import util

MAX_TRIAL = 3


def pull(sid, https=False):
    git_config = load_config()
    git_tools.ssh_key_path = git_config['ssh_key_path']
    roster_path = path.rosters_path / git_config['roster_file']
    roster = util.load_csv(roster_path)

    try:
        git_tools.cache_git_credential()

        if sid is None:
            for i_student in roster.values():
                pull_once(student_info=i_student, https=https)
        else:
            pull_once(student_info=roster[sid], https=https, everyone=False)

    finally:
        git_tools.uncache_git_credential()


def load_config():
    git_config_path = path.config_path / 'git_config.json'
    with open(git_config_path, 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['git_config']


def pull_once(student_info, https=False, everyone=True):
    trial = 0
    last_name = student_info['last_name'].lower()
    first_name = student_info['first_name'].lower()
    git_ssh_url = student_info['git_ssh']
    repo_name = student_info['repo_name']
    folder_name = last_name + '_' + first_name
    folder_path = path.homework_path / folder_name
    repo_path = folder_path / repo_name

    if https:
        git_pull = git_tools.git_https_pull
        git_clone = git_tools.git_https_clone
        git_url = git_tools.git_ssh_to_https(git_ssh_url)
    else:
        git_pull = git_tools.git_ssh_pull
        git_clone = git_tools.git_ssh_clone
        git_url = git_ssh_url

    print(first_name + " " + last_name + ":")

    print("Trying to directly pull it...")
    if git_pull(repo_path) == 0:
        print()
        return

    print("Failed to pull the repo of this student.")
    print("Trying to re-clone it...")
    util.del_folder(folder_path)

    while (git_clone(folder_path, git_url) != 0) and (trial < MAX_TRIAL):
        print("Failed to clone the repo of this student.")
        print("Re-cloning...")
        util.del_folder(folder_path)
        trial += 1

    if trial >= 3 and everyone:
        print("\nUnsolvable error.")

        while True:
            continue_flag = input("Continue (y/n)? ")

            if continue_flag == "y" or continue_flag == "Y":
                break
            elif continue_flag == "n" or continue_flag == "N":
                exit(0)

    print()


if __name__ == "__main__":
    m_parser = argparse.ArgumentParser()
    m_parser.add_argument('-i', '--id', help='pull a particular repository with the given student id')
    m_parser.add_argument('--https', action='store_true', help='pull the repository(ies) using https urls')
    m_args = m_parser.parse_args()

    pull(sid=m_args.id, https=m_args.https)
