#!/usr/bin/env python
import sys
import re

import scorelib

if (len(sys.argv) == 1):
	print("The first command line argument must be a text file for the script to read.")
	print("E.g. scorelib.txt")
	sys.exit()

prints = scorelib.load(sys.argv[1])

for p in prints:
	p.format()
	print("")


