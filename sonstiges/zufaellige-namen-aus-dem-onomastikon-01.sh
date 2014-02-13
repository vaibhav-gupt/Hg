#!/bin/sh

wget -m -np http://tekeli.li/onomastikon/ 
cd tekeli.li/onomastikon/
grep \<td\> -r */ |sed "s/<td>//" | sed "s/<\/td>//" > alle-namen.txt
    
python3 -c '
def is_good_line(l): 
        return l.split(":")[1:] and (
        not "Male" in l and  
        not "Female" in l and  
        not "nbsp" in l and  
        not "href" in l and  
        not "Surname" in l and  
        not "index." in l and  
        not "ources." in l and  
        not "otes." in l and 
        not "ntro." in l and 
        not ".html" in l.split(":")[1] and  
        not "/" in l.split(":")[1] and  
        not "+" in l.split(":")[1] and  
        not "-" in l.split(":")[1] and  
        not ";" in l and # letters which couldn’t be unescaped.
        not "<FONT" in l and 
        not " yr" in l and
        not "son of " in l.split(":")[1] and  
        l.split(":")[1].lstrip() and  
        not l.split(":")[2:]
        )


 
import re, html.entities
import logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(levelname)s (%(filename)s::%(lineno)s): %(message)s")


##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text.
# thanks to http://effbot.org/zone/re-sub.htm#unescape-html

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(html.entities.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)    



logging.info("Getting all good names from alle-namen.txt")
with open("alle-namen.txt", encoding="ISO-8859-15") as namen: 
        names = []
        for line in (line for line in (unescape(l) for l in namen)):
            if not is_good_line(line):
               logging.debug("not a good line: " + line)
               continue
            try:
               i,j = line.split(":")
            except ValueError as e:
               print(e)
               continue
            names.append((j,i))
    


logging.info("Writing " + str(len(names)) + " good names into alle-namen-vorne.txt")
with open("alle-namen-vorne.txt", "w", encoding="utf-8") as f:  
        for i,j in names:  
            k = i[:-2] + "            " + j + "\n"
            f.write(k.lstrip())


'

cp alle-namen-vorne.txt ../../

# 12 zufällige Namen rausholen: 
echo "cat alle-namen-vorne.txt | shuf | head -n 12"
cat alle-namen-vorne.txt | shuf | head -n 12
