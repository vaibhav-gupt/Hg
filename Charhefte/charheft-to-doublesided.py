#!/usr/bin/env python
# convert a charheft to landscape

import sys
import subprocess as sub
if not sys.argv[2:] or "--usage" in sys.argv:
  print( "usage " + sys.argv[0] + " infile outfile")
  print sys.argv
  sys.exit(0)

infile = sys.argv[1]
outfile = sys.argv[2]

sub.call(["pdfnup", "--landscape", "--nup", "2x1", "--outfile", outfile, "--", infile])
