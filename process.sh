#!/bin/bash
source /home/pi/.virtualenvs/cv/bin/activate
python /home/pi/image-processing/cv/process.py "$1" "$2" "$3"

