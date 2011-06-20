#!/bin/sh
# turn the 2.3.8 pdf into the 2.4 pdf with license and charsheet.

## Screen Versions
#pdfjoin ../../releases/1w6-regeln-2.4.0.pdf ../GPLv3.pdf ../../releases/charheft-vobsy.pdf --outfile ews-dok-2.4.0.pdf
pdfjoin --no-landscape  --rotateoversize 'false' ../../releases/1w6-regeln-2.5.3.pdf ../../releases/charheft-vobsy.pdf --outfile 1w6-regeln-2.5.3.pdf
pdfjoin --no-landscape  --rotateoversize 'false' ../../releases/1w6-regeln-2.5.3.pdf ../GPLv3.pdf ../../releases/charheft-vobsy.pdf --outfile 1w6-regeln-2.5.3-mit-lizenz.pdf

## Booklet
pdfnup --no-landscape --nup 1x1 --outfile part1.pdf --  ../../releases/1w6-regeln-2.5.3.pdf  1-24; pdfnup --no-landscape --nup 1x1 --outfile part2.pdf -- ../../releases/1w6-regeln-2.5.3.pdf 25-48; pdfnup --no-landscape --nup 1x1 --outfile gpl-1.pdf -- ../GPLv3.pdf 1-2; pdfnup --no-landscape --nup 1x1 --outfile gpl-2.pdf --  ../GPLv3.pdf 3-4; pdfnup --no-landscape  --nup 1x1 --outfile charheft.pdf -- ../../releases/charheft-vobsy.pdf  2,3,4,1; pdfjoin part1.pdf gpl-1.pdf charheft.pdf gpl-2.pdf part2.pdf --outfile test.pdf
./write_booklet_pdfjam.py test.pdf 1w6-regeln-2.5.3-booklet.pdf
