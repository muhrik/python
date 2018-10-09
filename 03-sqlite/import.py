#!/usr/bin/env python
import sys
import sqlite3

if (len(sys.argv) == 1):
	print("The first command line argument must be a text file for the script to read.")
	print("E.g. scorelib.txt")
	sys.exit()
if (len(sys.argv) == 2):
	print("The second command line argument is the output SQLite file.")
	sys.exit()

conn = sqlite3.connect("scorelib.dat")

#TODO continue
