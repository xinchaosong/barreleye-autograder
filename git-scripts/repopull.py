#!/usr/bin/env python

import sys
import os
import subprocess
import json
import pandas as pd

ssh_key_path = None
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


def repopull(clone_flag):
    global ssh_key_path
    global max_trial

    git_config = load_config()
    ssh_key_path = git_config['ssh_key_path']
    roster_csv = git_config['roster_csv']
    roster = pd.read_csv(os.path.join(os.path.dirname(__file__), roster_csv))

    for sid in range(roster.shape[0]):
        trial = 0
        last_name = str(roster.iloc[sid]['last_name'])
        first_name = str(roster.iloc[sid]['first_name'])
        git_ssh = str(roster.iloc[sid]['git_ssh'])
        repo_name = str(roster.iloc[sid]['repo_name'])
        folder_name = last_name.lower() + '_' + first_name.lower()
        repo_path = folder_name + '/' + repo_name

        print(first_name + " " + last_name + ":")

        if not clone_flag:
            if git_pull(repo_path) == 0:
                print()
                continue
            else:
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
    if len(sys.argv) == 1:
        repopull(False)

    elif len(sys.argv) == 2 and sys.argv[1] == "-c":
        repopull(True)

    else:
        print("usage:")
        print("repopull.py: pull all repos.")
        print("repopull.py -c: clone all repos.")
        exit(1)
