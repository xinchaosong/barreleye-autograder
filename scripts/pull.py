#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import argparse
import json
import subprocess

from scripts import path
from scripts import util

MAX_TRIAL = 3
g_ssh_key_path = ""


def load_config():
    git_config_path = path.config_path / 'git_config.json'
    with open(git_config_path, 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['git_config']


def git_clone(folder_path, git_ssh):
    command = "eval `ssh-agent -s` " \
              "&& ssh-add %s " \
              "&& mkdir %s " \
              "&& cd %s " \
              "&& git clone %s" \
              % (g_ssh_key_path, folder_path, folder_path, git_ssh)

    return subprocess.call(command, shell=True)


def git_pull(repo_path):
    command = "eval `ssh-agent -s` " \
              "&& ssh-add %s " \
              "&& cd %s " \
              "&& git checkout . " \
              "&& git pull" \
              % (g_ssh_key_path, repo_path)

    return subprocess.call(command, shell=True)


def pull_once(student_info, is_all=True):
    trial = 0
    last_name = student_info['last_name'].lower()
    first_name = student_info['first_name'].lower()
    git_ssh = student_info['git_ssh']
    repo_name = student_info['repo_name']
    folder_name = last_name + '_' + first_name
    folder_path = path.homework_path / folder_name
    repo_path = folder_path / repo_name

    print(first_name + " " + last_name + ":")

    if git_pull(repo_path) == 0:
        print()
        return

    print("Failed to pull the repo of this student.")
    print("Trying to re-clone it...")
    util.del_folder(folder_path)

    while (git_clone(folder_path, git_ssh) != 0) and (trial < MAX_TRIAL):
        print("Failed to clone the repo of this student.")
        print("Re-cloning...")
        util.del_folder(folder_path)
        trial += 1

    if trial >= 3 and is_all:
        print("\nUnsolvable error.")

        while True:
            continue_flag = input("Continue (y/n)? ")

            if continue_flag == "y" or continue_flag == "Y":
                break
            elif continue_flag == "n" or continue_flag == "N":
                exit(0)

    print()


def pull(sid):
    global g_ssh_key_path

    git_config = load_config()
    g_ssh_key_path = git_config['ssh_key_path']
    roster_path = path.rosters_path / git_config['roster_file']
    roster = util.load_csv(roster_path)

    if sid is None:
        for i_student in roster.values():
            pull_once(student_info=i_student)
    else:
        pull_once(student_info=roster[sid], is_all=False)


if __name__ == "__main__":
    m_parser = argparse.ArgumentParser()
    m_parser.add_argument('-i', '-id')
    m_args = m_parser.parse_args()

    pull(sid=m_args.i)
