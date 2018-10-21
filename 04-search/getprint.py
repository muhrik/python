#!/usr/bin/env python
import sys
import sqlite3

if (len(sys.argv) == 1):
	print("The first command line argument must be a print number.")
	print("E.g. \"645\"")
	sys.exit()

conn = sqlite3.connect("scorelib.dat")
cur = conn.cursor()

cur.execute('''select * from print where id = ?''', (sys.argv[1],))
p = cur.fetchone()
if (p == None):
	print("Print with number " + sys.argv[1] + " does not exist.")
	sys.exit()
cur.execute('''select * from edition where id = ?''', (p[2],))
e = cur.fetchone()
if (e == None):
	raise Exception("DB error while getting the edition!")
	sys.exit()
cur.execute('''select * from score where id = ?''', (e[1],))
s = cur.fetchone()
if (s == None):
	raise Exception("DB error while getting the score!")
	sys.exit()
cur.execute('''select * from score_author where score = ?''', (s[0],))
authors = cur.fetchall()

print("[")
for i in range(0, len(authors)):
	a = authors[i]
	cur.execute('''select * from person where id = ?''', (a[2],))
	person = cur.fetchone()

	if (i < len(authors) -1):
		listEnder = ","
	else:
		listEnder = ""

	if (person == None):
		raise Exception("DB error while getting the composer!")
		sys.exit()
	if (str(person[1]) == "NULL" and str(person[2]) == "NULL"):
		print("\t{ \"name\": \"" + person[3] + "\"" + " }" + listEnder)
	else:
		print("\t{ \"name\": \"" + person[3] + "\",")	
	if (str(person[1]) != "NULL" and str(person[2]) != "NULL"):
		print("\t  \"born\": " + str(person[1]) + ", " + "\"died\": " + str(person[2]) + " }" + listEnder)
	if (str(person[1]) != "NULL" and str(person[2]) == "NULL"):
		print("\t  \"born\": " + str(person[1]) + " }" + listEnder)

print("]")
