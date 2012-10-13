#!/bin/sh
#
# Author: Sven Hartenstein http://www.svenhartenstein.de/Software/A5-booklets
#
# This script takes an A5 latex file as input and produces an A4
# document (both ps and pdf) for printing an A5 booklet
#
# Usage:
# booklet [filename without extension]

latex -shell-escape $1
latex -shell-escape $1

# make an a5 ps from dvi:
dvips -t a5 -o $1.ps $1.dvi

# sort pages
psbook $1.ps tmp1.ps

# put two pages on one a4 sheet
psnup -Pa5 -pa4 -2 tmp1.ps tmp2.ps

# change a5 to a4 in ps file
sed 's/^%%DocumentPaperSizes: A5/%%DocumentPaperSizes: a4/g' < tmp2.ps > $1_booklet.ps

# produce pdf files, pdflatex ist used (twice) to get bookmarks
pdflatex -shell-escape $1.tex
pdflatex -shell-escape $1.tex
ps2pdf -sPAPERSIZE=a4 $1_booklet.ps

# delete tmp files
rm tmp1.ps tmp2.ps
