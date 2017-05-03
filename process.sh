#!/bin/bash
source ~/.virtualenvs/cv/bin/activate
python process.py "$1" "$2" "$3"
