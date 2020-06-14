#!/bin/bash

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

if [ -n "$1" ] && [ "$1" == 'pull' ]; then
  python3 "$PWD"/scripts "$@"
else
  python3 "$PWD"/scripts grade "$@"
fi
