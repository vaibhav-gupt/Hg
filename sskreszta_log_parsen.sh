#!/bin/sh
# Build the Sskreszta Log site. 
# License of this script: GPL

echo "entering folder RaumZeit/Charaktere/Sskreszta/"
cd RaumZeit/Charaktere/Sskreszta/
mkdir -p static

# First create the markdown content of the index page. 

echo "building index page"
echo "Sskreszta-Log statisch" > static/index.mdwn
echo "======================" >> static/index.mdwn
for i in Sskreszta-log*txt Stationen_unserer_Reise.txt
  do echo "[$i]($i.html)" >> static/index.mdwn
  echo "" >> static/index.mdwn
done

# Then compile it to html. 

echo "compiling it to html"
echo "<html><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/></head><body text='#903r09'>" > static/index.html
markdown -e utf-8 static/index.mdwn >> static/index.html || markdown-python -e utf-8 static/index.mdwn >> static/index.html || markdown.py -e utf-8 static/index.mdwn >> static/index.html
echo "<p>- <a href='http://1w6.org'>zur Hauptseite</a> -</p></body></html>" >> static/index.html

# And compile every entry to html. 

echo "compile every entry to html"
for i in Sskreszta-log* Stationen_unserer_Reise.txt
  do echo "<html>" > static/$i.html
  echo "<head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/></head>" >> static/$i.html
  echo "<body text='#903r09'>" >> static/$i.html
  markdown $i >> static/$i.html || markdown-python $i >> static/$i.html || markdown.py $i >> static/$i.html
  echo "<a href='index.html'>andere Logeinträge</></body></html>" >> static/$i.html
done

# Also turn the dot file into the travel diagram (png)
echo "./aufruf_dot_zu_png.sh"
./aufruf_dot_zu_png.sh
# And copy the current dot file into static
cp stationen_unserer_reise.dot static/
