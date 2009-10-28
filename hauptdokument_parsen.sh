#!/bin/sh

# a rather complex parse_and_list_markdown_files.py call :)

parse_and_list_markdown_files.py --preprocessor "lines = markdown_data.splitlines()
for l in lines:
 _l = l
 while _l and _l[-1] == ' ':
  _l = _l[:-1] # remove trailing whitespace
 _l = _l + '  ' # add exactly two spaces, since we don't want to concatenate lines
 if _l.startswith('**'):
  _l = _l[:-2] + '**  '
 elif _l.startswith('*'):
  _l = _l[:-2] + '*  '
 elif _l.startswith('<fuss>'):
  _l = '<small>' + _l[6:-2] + '</small>  '
 lines[lines.index(l)] = _l
markdown_data = '\n'.join(lines)
" "Ein Wuerfel System" Hauptdokument/Scribus-Quellen http://1w6.org/deutsch/regeln/quellen
