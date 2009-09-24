#!/bin/sh
# Build the Sskreszta Log site. 
# License of this script: GPL

echo "entering folder RaumZeit/Charaktere/Sskreszta/"
cd RaumZeit/Charaktere/Sskreszta/

# First create the markdown content of the index page. 
parse_and_list_markdown_files.py "Sskreszta-Log statisch" . http://1w6.org

# Also turn the dot file into the travel diagram (png)
echo "./aufruf_dot_zu_png.sh"
./aufruf_dot_zu_png.sh
# And copy the current dot file into static
cp stationen_unserer_reise.dot static/
