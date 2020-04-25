#!/bin/bash

# Created by Xinchao Song, contact@xinchaosong.com.
# April 21, 2020
# Copyright © 2020 Xinchao Song. All rights reserved.

if [ -n "$1" ]; then
  if [ -n "$2" ]; then
    python3 grade.py -i "$1" "$2"
  else
    python3 grade.py -i "$1"
  fi
else
  python3 grade.py
fi

if [ -n "$1" ]; then
  python3 repopull.py -i "$1"
else
  python3 repopull.py
fi