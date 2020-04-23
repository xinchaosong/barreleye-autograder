#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import os
import subprocess
import argparse
import json

import pandas as pd

ssh_key_path = None
roster = None
max_trial = 3


def load_config():
    with open("git_config.json", 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['git_config']


def git_clone(folder_name, git_ssh):
    global ssh_key_path

    command = "eval `ssh-agent -s` " \
              "&& ssh-add %s " \
              "&& mkdir %s " \
              "&& cd %s " \
              "&& git clone %s" \
              % (ssh_key_path, folder_name, folder_name, git_ssh)

    return subprocess.call(command, shell=True)


def git_pull(repo_path):
    global ssh_key_path

    command = "eval `ssh-agent -s` " \
              "&& ssh-add %s " \
              "&& cd %s " \
              "&& git checkout . " \
              "&& git pull" \
              % (ssh_key_path, repo_path)

    return subprocess.call(command, shell=True)


def del_folder(folder_name):
    return subprocess.call("rm -rf %s" % folder_name, shell=True)


def pull_repo(sid):
    trial = 0
    last_name = str(roster.loc[sid, 'last_name'])
    first_name = str(roster.loc[sid, 'first_name'])
    git_ssh = str(roster.loc[sid, 'git_ssh'])
    repo_name = str(roster.loc[sid, 'repo_name'])
    folder_name = last_name.lower() + '_' + first_name.lower()
    repo_path = folder_name + '/' + repo_name

    print(first_name + " " + last_name + ":")

    if git_pull(repo_path) == 0:
        print()
        return

    print("Failed to pull the repo of this student.")
    print("Trying to re-clone it...")
    del_folder(folder_name)

    while git_clone(folder_name, git_ssh) != 0 and trial < max_trial:
        print("Failed to clone the repo of this student.")
        print("Re-cloning...")
        del_folder(folder_name)
        trial += 1

    if trial >= 3:
        print("\nUnsolvable error.")

        while True:
            continue_flag = input("Continue (y/n)? ")

            if continue_flag == "y" or continue_flag == "Y":
                break
            elif continue_flag == "n" or continue_flag == "N":
                exit(0)

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-id', type=int)
    args = parser.parse_args()

    m_sid = args.i

    git_config = load_config()
    ssh_key_path = git_config['ssh_key_path']
    roster_csv = git_config['roster_csv']
    roster = pd.read_csv(os.path.join(os.path.dirname(__file__), roster_csv), index_col=0)

    if m_sid is None:
        for s in range(roster.shape[0]):
            pull_repo(s)
    else:
        pull_repo(int(m_sid))
