#!/bin/sh
# thanks to Heiner: http://www.virtualzone.de/2012/11/how-to-reduce-pdf-file-size-in-linux.html
gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -sOutputFile=zettel-small-gs.pdf zettel.pdf

