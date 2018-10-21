#!/usr/bin/env python
import sys
import sqlite3

if (len(sys.argv) == 1):
	print("The first command line argument must be a string to search for.")
	print("E.g. \"Bach\"")
	sys.exit()

conn = sqlite3.connect("scorelib.dat")
cur = conn.cursor()

arg = "%" + sys.argv[1] + "%"
cur.execute('''select * from person where person.name like ?''', (arg,))
people = cur.fetchall()
if (people == None or len(people) == 0):
	raise Exception("No people with such substring in their name found!")
	sys.exit()

print("[")
for i in range(0, len(people)):
	person = people[i]
	personID = person[0]
	personBorn = person[1]
	personDied = person[2]
	personName = person[3]
	cur.execute('''select * from score_author where composer = ?''', (personID,))
	score_authors = cur.fetchall()
	if (score_authors == None or len(score_authors) == 0):
		#This person hasn't composed anything!
		continue
	print(" {")
	print("  \"" + personName + "\": [")
	for j in range(0, len(score_authors)):
		score_author = score_authors[j]
		if (j < len(score_authors) -1):
			listEnderj = ","
		else:
			listEnderj = ""

		scoreID = score_author[1]
		cur.execute('''select * from score where id = ?''', (scoreID,))
		score = cur.fetchone()
		if (score == None):
			raise Exception("DB error while getting the score!")
			sys.exit()
		scoreName = score[1]
		scoreGenre = score[2]
		if (scoreGenre == ""):
			scoreGenre = "NULL"
		scoreKey = score[3]
		if (scoreKey == ""):
			scoreKey = "NULL"
		scoreIncipit = score[4]
		if (scoreIncipit == ""):
			scoreIncipit = "NULL"
		scoreYear = score[5]
		cur.execute('''select * from edition where score = ?''', (scoreID,))
		edition = cur.fetchone()
		if (edition == None):
			raise Exception("DB error while getting the edition!")
			sys.exit()
		editionID = edition[0]
		editionName = edition[2]
		if (editionName == ""):
			editionName = "NULL"
		editionYear = edition[3]
		cur.execute('''select * from print where edition = ?''', (editionID,))
		prnt = cur.fetchone()
		if (prnt == None):
			raise Exception("DB error while getting the print!")
			sys.exit()
		printID = prnt[0]
		partiture = prnt[1]
		if (partiture == "Y"):
			partiture = "true"
		if (partiture == "N"):
			partiture = "false"

		cur.execute('''select * from voice where score = ?''', (scoreID,))
		voices = cur.fetchall()
		if (voices == None):
			raise Exception("DB error while getting the voices!")
			sys.exit()

		cur.execute('''select * from edition_author where edition = ?''', (editionID,))
		edition_authors = cur.fetchall()
		if (edition_authors == None):
			raise Exception("DB error while getting the voices!")
			sys.exit()

		cur.execute('''select * from score_author where score = ?''', (scoreID,))
		composers = cur.fetchall()
		if (composers == None):
			raise Exception("DB error while getting the composers!")
			sys.exit()
		
		print("   { \"Print number\": " + str(printID) + ",")
		print("     \"Composers\": [")
		for k in range(0, len(composers)):
			if (k < len(composers) -1):
				listEnderk = ","
			else:
				listEnderk = ""
			composer = composers[k]
			cur.execute('''select * from person where id = ?''', (composer[2],))
			cmpser = cur.fetchone()
			if (cmpser == None):
				raise Exception("DB error while getting the composer!")
				sys.exit()
			print("       { " + "\"name\": \"" + cmpser[3] + "\", \"born\": " + str(cmpser[1]) + ", \"died\": " + str(cmpser[2]) + " }" + listEnderk)
		print("     ],")
		print("     \"Title\": " + scoreName + ",")
		print("     \"Genre\": " + scoreGenre + ",")
		print("     \"Key\": " + scoreKey + ",")
		print("     \"Composition Year\": " + str(scoreYear) + ",")
		print("     \"Publication Year\": " + str(editionYear) + ",")
		print("     \"Edition\": " + editionName + ",")
		print("     \"Editors\": [")
		for k in range(0, len(edition_authors)):
			if (k < len(edition_authors) -1):
				listEnderk = ","
			else:
				listEnderk = ""
			editor = edition_authors[k]
			cur.execute('''select * from person where id = ?''', (editor[2],))
			edtr = cur.fetchone()
			if (cmpser == None):
				raise Exception("DB error while getting the editor!")
				sys.exit()
			print("       { " + "\"name\": \"" + edtr[3] + "\", \"born\": " + str(edtr[1]) + ", \"died\": " + str(edtr[2]) + " }" + listEnderk)
		print("     ],")
		print("     \"Voices\": {")
		for k in range(0, len(voices)):
			if (k < len(voices) -1):
				listEnderk = ","
			else:
				listEnderk = ""
			voice = voices[k]
			print("         \"" + str(voice[1]) + "\": { \"name\": \"" + voice[4] + "\", \"range\": \"" + voice[3] + "\" }" + listEnderk)
		print("     },")
		print("     \"Partiture\": " + partiture + ",")
		print("     \"Incipit\": " + scoreIncipit + " }" + listEnderj)
	if (i < len(people) -1):
		listEnderi = ","
	else:
		listEnderi = ""
	print("  ]" + listEnderi)
	print(" }" + listEnderi)

print("]")
