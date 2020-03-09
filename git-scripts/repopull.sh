#!/bin/bash

if [ -n "$1" ]; then
    python3 repopull.py "$1"
else
    python3 repopull.py
fi
