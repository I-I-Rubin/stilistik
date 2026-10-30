#!/usr/bin/env zsh

# curl https://marxists.catbull.com/archive/marx/works/1861/economic/ch12.htm | iconv -f latin1 -t utf8 > ltr.html
#    
# pandoc -r html -w markdown ltr.html -o ltr.txt
#cp untitled.tex $TEXT.tex t What they are saying is this, that they are prepared to destroy the planet, such is their rage.
# pandoc -r markdown -w latex $TEXT.txt -o untitled_.tex 

cd ..
result=${PWD##*/}
cd pdf
cp ../*_en.md untitled.txt
pandoc -r markdown -w latex untitled.txt  --wrap=none -o untitled_.tex 
perl -CSD -0pi -e 's/\\footnote\{/\\footnote\{~/g' untitled_.tex 
lualatex untitled.tex  
mv untitled.pdf $result.pdf
open $result.pdf