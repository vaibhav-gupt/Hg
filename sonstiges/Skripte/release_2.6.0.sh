#!/bin/sh
# turn the 2.3.8 pdf into the 2.4 pdf with license and charsheet.

## Screen Versions
#pdfjoin ../../releases/1w6-regeln-2.4.0.pdf ../GPLv3.pdf ../../releases/charheft-vobsy.pdf --outfile ews-dok-2.4.0.pdf
pdfjoin --no-landscape  --rotateoversize 'false' ../../releases/cover-tim-front-2.6.0.pdf ../../releases/1w6-regeln-2.6.0.pdf ../../releases/cover-tim-back-2.6.0.pdf ../../releases/charheft-vobsy.pdf --outfile 1w6-regeln-2.6.0.pdf
pdfjoin --no-landscape  --rotateoversize 'false' ../../releases/cover-tim-front-2.6.0.pdf ../../releases/1w6-regeln-2.6.0.pdf ../../releases/cover-tim-back-2.6.0.pdf ../GPLv3-4-seiten.pdf ../../releases/charheft-vobsy.pdf --outfile 1w6-regeln-2.6.0-mit-lizenz.pdf

## Booklet
pdfnup --no-landscape --nup 1x1 --outfile part0.pdf -- ../../releases/cover-tim-front-2.6.0.pdf
pdfnup --no-landscape --nup 1x1 --outfile part1.pdf --  ../../releases/1w6-regeln-2.6.0.pdf  2-24
 pdfnup --no-landscape --nup 1x1 --outfile part2.pdf -- ../../releases/1w6-regeln-2.6.0.pdf 25-47
pdfnup --no-landscape --nup 1x1 --outfile part3.pdf -- ../../releases/cover-tim-back-2.6.0.pdf
 pdfnup --no-landscape --nup 1x1 --outfile gpl-1.pdf -- ../GPLv3-4-seiten.pdf 1-2
 pdfnup --no-landscape --nup 1x1 --outfile gpl-2.pdf --  ../GPLv3-4-seiten.pdf 3-4
 pdfnup --no-landscape  --nup 1x1 --outfile charheft.pdf -- ../../releases/charheft-vobsy.pdf  2,3,4,1
 pdfjoin part0.pdf  part1.pdf gpl-1.pdf charheft.pdf gpl-2.pdf part2.pdf part3.pdf --outfile test.pdf
./write_booklet_pdfjam.py test.pdf 1w6-regeln-2.6.0-booklet.pdf
