#!/bin/sh

wget -m http://www.gaminggeeks.org/Resources/KateMonk/
cd www.gaminggeeks.org/Resources/KateMonk/
grep \<td\> -r */ |sed "s/<td>//" | sed "s/<\/td>//" > alle-namen.txt
    
python -c '
def is_good_line(l): 
        return l.split(":")[1:] and (
        not "Male" in l and  
        not "Female" in l and  
        not ".html" in l and  
        not "nbsp" in l and  
        not "href" in l and  
        not "Surname" in l and  
        not ".shtml" in l and  
        not "Sources.htm" in l and  
        not "/" in l and  
        not "+" in l and  
        not l.split(":")[2:]
        )
    
    
with open("alle-namen.txt") as namen: 
        names = [(j,i) for i,j in [line.split(":")  
                 for line in namen if is_good_line(line)]]
    
with open("alle-namen-vorne.txt", "w") as f:  
        for i,j in names:  
            k = i[:-2] + "      " + j + "\n"  
            f.write(k.lstrip())
'

cp alle-namen-vorne.txt ../../../

# 12 zufällige Namen rausholen: 
# cat alle-namen-vorne.txt | shuf | head -n 12
