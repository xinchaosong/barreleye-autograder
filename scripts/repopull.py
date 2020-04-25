#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import argparse
import json
import subprocess

from scripts import util

MAX_TRIAL = 3
g_ssh_key_path = ""


def load_config():
    with open("../config/git_config.json", 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['git_config']


def git_clone(folder_name, git_ssh):
    command = "eval `ssh-agent -s` " \
              "&& ssh-add %s " \
              "&& mkdir %s " \
              "&& cd %s " \
              "&& git clone %s" \
              % (g_ssh_key_path, folder_name, folder_name, git_ssh)

    return subprocess.call(command, shell=True)


def git_pull(repo_path):
    command = "eval `ssh-agent -s` " \
              "&& ssh-add %s " \
              "&& cd %s " \
              "&& git checkout . " \
              "&& git pull" \
              % (g_ssh_key_path, repo_path)

    return subprocess.call(command, shell=True)


def del_folder(folder_name):
    subprocess.call("rm -rf %s" % folder_name, shell=True)


def pull_repo(student_info, is_all=True):
    trial = 0
    last_name = student_info['last_name'].lower()
    first_name = student_info['first_name'].lower()
    git_ssh = student_info['git_ssh']
    repo_name = student_info['repo_name']
    folder_name = last_name + '_' + first_name
    repo_path = folder_name + '/' + repo_name

    print(first_name + " " + last_name + ":")

    if git_pull(repo_path) == 0:
        print()
        return

    print("Failed to pull the repo of this student.")
    print("Trying to re-clone it...")
    del_folder(folder_name)

    while (git_clone(folder_name, git_ssh) != 0) and (trial < MAX_TRIAL):
        print("Failed to clone the repo of this student.")
        print("Re-cloning...")
        del_folder(folder_name)
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


def repopull(sid):
    global g_ssh_key_path

    git_config = load_config()
    g_ssh_key_path = git_config['ssh_key_path']
    roster = util.load_csv(git_config['roster_path'])

    if sid is None:
        for i_student in roster.values():
            pull_repo(student_info=i_student)
    else:
        pull_repo(student_info=roster[sid], is_all=False)


if __name__ == "__main__":
    m_parser = argparse.ArgumentParser()
    m_parser.add_argument('-i', '-id')
    m_args = m_parser.parse_args()

    repopull(sid=m_args.i)
