#!/bin/bash

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

if [ -n "$1" ]; then
  python3 repopull.py "$1"
else
  python3 repopull.py
fi
