#!/bin/sh
# Build the Sskreszta Log site. 
# License of this script: GPL

cd RaumZeit/Charaktere/Sskreszta/
mkdir -p static
echo "Sskreszta-Log statisch" > static/index.mdwn
echo "======================" >> static/index.mdwn
for i in Sskreszta-log*txt
  do echo "[$i]($i.html)" >> static/index.mdwn
  echo "" >> static/index.mdwn
done

markdown.py -e utf-8 static/index.mdwn > static/index.html
for i in Sskreszta-log*
  do echo "<html>" > static/$i.html
  echo "<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>" >> static/$i.html
  echo "<body>" >> static/$i.html
  markdown.py $i >> static/$i.html
  echo "</body></html>" >> static/$i.html
done

