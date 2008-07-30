#!/bin/sh
# Build the Sskreszta Log site. 
# License of this script: GPL

cd RaumZeit/Charaktere/Sskreszta/
mkdir -p static

# First create the markdown content of the index page. 

echo "Sskreszta-Log statisch" > static/index.mdwn
echo "======================" >> static/index.mdwn
for i in Sskreszta-log*txt
  do echo "[$i]($i.html)" >> static/index.mdwn
  echo "" >> static/index.mdwn
done

# Then compile it to html. 

echo "<html><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/></head><body text='#903r09'>" > static/index.html
markdown.py -e utf-8 static/index.mdwn >> static/index.html
echo "<p>- <a href='http://1w6.org'>zur Hauptseite</a> -</p></body></html>" >> static/index.html

# And compiile every entry to html. 

for i in Sskreszta-log*
  do echo "<html>" > static/$i.html
  echo "<head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/></head>" >> static/$i.html
  echo "<body text='#903r09'>" >> static/$i.html
  markdown.py $i >> static/$i.html
  echo "<a href='index.html'>andere Logeinträge</></body></html>" >> static/$i.html
done

