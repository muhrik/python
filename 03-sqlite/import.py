#!/usr/bin/env python
import sys
import sqlite3
import scorelib.py

if (len(sys.argv) == 1):
	print("The first command line argument must be a text file for the script to read.")
	print("E.g. scorelib.txt")
	sys.exit()
if (len(sys.argv) == 2):
	print("The second command line argument is the output SQLite file.")
	sys.exit()

load(sys.argv[1])

conn = sqlite3.connect(sys.argv[2])
cur = conn.cursor()

#TODO continue
#TODO 1) Create relevant tables using the schematics from scorelib.sql
#TODO 2) For all existing objects from load(), insert them into the tables

conn.commit()
