#!/usr/bin/env python

# Created by Xinchao Song, contact@xinchaosong.com.
# June 14, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

import subprocess
import sys
from pathlib import Path

from scripts import util

ssh_key_path = ""
git_credential_timeout = 3600
gitconfig_temp_file = '.gitconfig_barreleye'


def copy_gitconfig():
    gitconfig_src = Path.home() / '.gitconfig'
    gitconfig_dst = Path.home() / gitconfig_temp_file

    util.copy_file(gitconfig_src, gitconfig_dst)


def cache_git_credential():
    copy_gitconfig()

    command = "git config --global credential.helper 'cache --timeout=%d'" % git_credential_timeout

    return subprocess.call(command, shell=True)


def restore_gitconfig():
    gitconfig_src = Path.home() / gitconfig_temp_file
    gitconfig_dst = Path.home() / '.gitconfig'

    if gitconfig_src.exists():
        util.del_file(gitconfig_dst)
        util.copy_file(gitconfig_src, gitconfig_dst)
        util.del_file(gitconfig_src)


def uncache_git_credential():
    restore_gitconfig()

    command = "git credential-cache exit " \
              "&& git config --global --unset credential.helper 'cache'"

    return subprocess.call(command, shell=True)


def git_ssh_clone(folder_path, git_url):
    util.make_folder(folder_path)
    command = "cd %s " \
              "&& eval `ssh-agent -s` " \
              "&& ssh-add %s " \
              "&& git clone %s " \
              "&& ssh-agent -k" \
              % (folder_path, ssh_key_path, git_url)

    return subprocess.call(command, shell=True)


def git_ssh_pull(repo_path):
    command = "cd %s " \
              "&& eval `ssh-agent -s` " \
              "&& ssh-add %s " \
              "&& git checkout . " \
              "&& git pull " \
              "&& ssh-agent -k" \
              % (repo_path, ssh_key_path)

    return subprocess.call(command, shell=True)


def git_https_clone(folder_path, git_url):
    util.make_folder(folder_path)
    command = "cd %s " \
              "&& git clone %s " \
              % (folder_path, git_url)

    return subprocess.call(command, shell=True)


def git_https_pull(repo_path):
    command = "cd %s " \
              "&& git checkout . " \
              "&& git pull " \
              % repo_path

    return subprocess.call(command, shell=True)


def git_ssh_to_https(ssh_url):
    return ssh_url.replace(':', '/').replace("git@", "https://")
