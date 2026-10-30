#!/bin/zsh

source ~/.zprofile
cd ..
result=${PWD##*/} 
cp ${result}_en.md typst
cp ${result}_de.md typst
cd typst
python3 typst_table.py $result
typst compile $result.typ ${result}_typst.pdf
open ${result}_typst.pdf
