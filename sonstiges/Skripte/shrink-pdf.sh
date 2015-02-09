#!/bin/bash

# thanks to http://linuxaria.com/howto/parse-options-in-your-bash-script-with-getopt
# TODO: replace by getopts as in http://stackoverflow.com/a/7680682/7666
PARSED_OPTIONS=$(getopt -n "$0"  -o hl: --long "help,level:"  -- "$@")
PROGRAM_NAME="$0"

# error out on failure
if [ $? -ne 0 ]; then exit 1; fi

# getopt magic
eval set -- "$PARSED_OPTIONS"

function help { # takes the program name as parameter ($1)
      echo "usage: $1 [-h] | [-l <level>] <infile> <outfile> or $1 [--help] | [--level <level>] <infile> <outfile>"
      echo ""
      echo "levels:
    screen   (screen-view-only quality, 72 dpi images)
    ebook    (low quality, 150 dpi images)
    printer  (high quality, 300 dpi images)
    prepress (high quality, color preserving, 300 dpi imgs)
    default  (almost identical to /screen)
    
for details, refer to gs: http://milan.kupcevic.net/ghostscript-ps-pdf/
"
      exit 0
}

while true;
do
  case "$1" in
 
    -h|--help)
     help "${PROGRAM_NAME}"
     shift;;
 
    -l|--level)
      if [ -n "$2" ];
      then
        level="$2"
      fi
      shift 2;;
 
    --)
      shift
      break;;
  esac
done

if [ $# -lt 2 ]; then
  help "${PROGRAM_NAME}"
fi

if [[ x"$level" == x"" ]]; then
  level="ebook"
fi

infile="$1"
outfile="$2"

echo gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/"$level" -sOutputFile="${outfile}" "${infile}"
gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/"$level" -sOutputFile="${outfile}" "${infile}"
