#!/bin/bash
source /home/pi/.virtualenvs/cv/bin/activate
python process.py "$1" "$2" "$3"

