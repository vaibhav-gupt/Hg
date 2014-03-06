#!/bin/sh
# turn the base pdf into the release with license and charsheet.

## Booklet
pdfnup --no-landscape --nup 1x1 --outfile part0.pdf -- ../../Hauptdokument/1w6-regeln-2.6.1i-cover.pdf 2
pdfnup --no-landscape --nup 1x1 --outfile part1.pdf -- ../../Hauptdokument/1w6-regeln-2.6.1i.pdf  2-24
pdfnup --no-landscape --nup 1x1 --outfile part2.pdf -- ../../Hauptdokument/1w6-regeln-2.6.1i.pdf 25-47
pdfnup --no-landscape --nup 1x1 --outfile part3.pdf -- ../../Hauptdokument/1w6-regeln-2.6.1i-cover.pdf 1
pdfnup --no-landscape --nup 1x1 --outfile gpl-1.pdf -- ../GPLv3-4-seiten.pdf 1-2
pdfnup --no-landscape --nup 1x1 --outfile gpl-2.pdf -- ../GPLv3-4-seiten.pdf 3-4
pdfnup --no-landscape  --nup 1x1 --outfile charheft.pdf -- ../../releases/charheft-vobsy.pdf  2,3,4,1
pdfjoin part0.pdf  part1.pdf gpl-1.pdf charheft.pdf gpl-2.pdf part2.pdf part3.pdf --outfile test.pdf
./write_booklet_pdfjam.py test.pdf 1w6-regeln-2.6.1i-booklet.pdf

## Screen Versions
# pdfjoin ../../releases/1w6-regeln-2.6.1i.pdf ../GPLv3.pdf ../../releases/charheft-vobsy.pdf --outfile ews-dok-2.6.1i.pdf
pdfjoin --no-landscape  --rotateoversize 'false' ../../Hauptdokument/1w6-regeln-2.6.1i-cover.pdf 2 ../../Hauptdokument/1w6-regeln-2.6.1i.pdf 2-48 ../../Hauptdokument/1w6-regeln-2.6.1i-cover.pdf 1 ../../releases/charheft-vobsy.pdf 1-4 --outfile 1w6-regeln-2.6.1i.pdf
pdfjoin --no-landscape  --rotateoversize 'false' ../../Hauptdokument/1w6-regeln-2.6.1i-cover.pdf 2 ../../Hauptdokument/1w6-regeln-2.6.1i.pdf 2-48 ../../Hauptdokument/1w6-regeln-2.6.1i-cover.pdf 1 ../GPLv3-4-seiten.pdf 1-4 ../../releases/charheft-vobsy.pdf 1-4 --outfile 1w6-regeln-2.6.1i-mit-lizenz.pdf

pdfnup --no-landscape --nup 1x1 --outfile part1-1.pdf --  ../../Hauptdokument/1w6-regeln-2.6.1i.pdf  1-24
 pdfnup --no-landscape --nup 1x1 --outfile part2-1.pdf -- ../../Hauptdokument/1w6-regeln-2.6.1i.pdf 25-48
 pdfjoin  part1-1.pdf gpl-1.pdf charheft.pdf gpl-2.pdf part2-1.pdf --outfile test.pdf
./write_booklet_pdfjam.py test.pdf 1w6-regeln-2.6.1i-booklet-weiss.pdf
