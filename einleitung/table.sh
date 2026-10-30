#!/bin/zsh

source ~/.zprofile
result=${PWD##*/} 
python table.py $result
sleep 1
open $result.html

#   