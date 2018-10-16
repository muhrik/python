#!/usr/bin/env python
import sys
import sqlite3

if (len(sys.argv) == 1):
	print("The first command line argument must be a string to search for.")
	print("E.g. \"Bach\"")
	sys.exit()

conn = sqlite3.connect("scorelib.dat")
