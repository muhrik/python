#!/usr/bin/env python
import sys
import sqlite3
import scorelib

if (len(sys.argv) == 1):
	print("The first command line argument must be a text file for the script to read.")
	print("E.g. scorelib.txt")
	sys.exit()
if (len(sys.argv) == 2):
	print("The second command line argument is the output SQLite file.")
	print("E.g. scorelib.dat")
	sys.exit()

prints = scorelib.load(sys.argv[1])

conn = sqlite3.connect(sys.argv[2])
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cur = conn.cursor()

# A table that stores a person: could be either a composer or an editor.
cur.execute('''create table person ( id integer primary key not null,
                      born integer,
                      died integer,
                      name varchar not null );''')

# Stores info about a single score. Since some of the scores in the library
# have multiple compositions in them, author data is stored in a separate
# table (score_author). The relationship between authors and scores is M:N
# since most composers have more than one composition to their name. Year in
# this table refers to the field 'Composition Year' in the text file.
cur.execute('''create table score ( id integer primary key not null,
                     name varchar,
                     genre varchar,
                     key varchar,
                     incipit varchar,
                     year integer );''')

# Information about the voices in a particular score. Scores often contain
# multiple voices, hence a separate table. The relationship is 1:N (each row
# in the voice table belongs to exactly one score). The 'number' column
# refers to the voice number, i.e. it's 1 for a line starting 'Voice 1:'.
cur.execute('''create table voice ( id integer primary key not null,
                     number integer not null, -- which voice this is
                     score integer references score( id ) not null,
                     range varchar,
                     name varchar );''')

# Multiple editions of a given score may exist, and any given edition could
# have multiple editors. Like with score -- author relationship, this is M:N
# and stored in an auxiliary table, edition_author.
cur.execute('''create table edition ( id integer primary key not null,
                       score integer references score( id ) not null,
                       name varchar,
                       year integer );''')

# Auxiliary table. See 'score'.
cur.execute('''create table score_author( id integer primary key not null,
                           score integer references score( id ) not null,
                           composer integer references person( id ) not null );''')

# Auxiliary table. See 'edition'.
cur.execute('''create table edition_author( id integer primary key not null,
                             edition integer references edition( id ) not null,
                             editor integer references person( id ) not null );''')

# Information about a printed score. This is always of a particular edition,
# so we refer to that. The partiture column describes whether a partiture is
# part of the print. In all the above tables, 'id' is an auto-generated
# primary key. For print, however, this is the value of the 'Print Number'
# field from the text file.
cur.execute('''create table print ( id integer primary key not null,
                     partiture char(1) default 'N' not null, -- N = No, Y = Yes, P = Partial
                     edition integer references edition( id ) );''')

for p in prints: #TODO - store only unique values for persons! Merge born/died!
	e = p.edition
	c = e.composition

	if (e.year == None):
		eYear = "NULL"
	else:
		eYear = str(e.year)
	if (c.year == None):
		cYear = "NULL"
	else:
		cYear = str(c.year)
	if (c.genre == None):
		cGenre = ""
	else:
		cGenre = str(c.genre)
	if (c.key == None):
		cKey = ""
	else:
		cKey = str(c.key)
	if (c.incipit == None):
		cIncipit = ""
	else:
		cIncipit = str(c.incipit)

	cur.execute('''insert into score (name, genre, key, incipit, year) values (?, ?, ?, ?, ?)''', (c.name, cGenre, cKey, cIncipit, cYear))
	cur.execute('SELECT last_insert_rowid()')
	scoreID = cur.fetchone()[0]
	print("Score " + str(scoreID) + " is OK!")

	for i in range(0, len(c.voices)):
		cur.execute('''insert into voice (number, score, range, name) values (?, ?, ?, ?)''', (i+1, scoreID, "NULL", c.voices[i].name))

	cur.execute('''insert into edition (score, name, year) values (?, ?, ?)''', (str(scoreID), e.name, eYear))
	cur.execute('SELECT last_insert_rowid()')
	editionID = cur.fetchone()[0]
	print("Edition " + str(editionID) + " is OK!")

	for person in c.authors:
		if (person.name == None or person.name == ""):
			continue
		if (person.born == None):
			pBorn = "NULL"
		else:
			pBorn = str(person.born)
		if (person.died == None):
			pDied = "NULL"
		else:
			pDied = str(person.died)
		cur.execute('''insert into person (born, died, name) values (?, ?, ?)''', (pBorn, pDied, person.name))
		cur.execute('SELECT last_insert_rowid()')
		personID = cur.fetchone()[0]
		cur.execute('''insert into score_author (score, composer) values (?, ?)''', (scoreID, personID))
	
	for person in e.authors:
		if (person.name == None or person.name == ""):
			continue
		if (person.born == None):
			pBorn = "NULL"
		else:
			pBorn = str(person.born)
		if (person.died == None):
			pDied = "NULL"
		else:
			pDied = str(person.died)
		cur.execute('''insert into person (born, died, name) values (?, ?, ?)''', (pBorn, pDied, person.name))
		cur.execute('SELECT last_insert_rowid()')
		personID = cur.fetchone()[0]
		cur.execute('''insert into edition_author (edition, editor) values (?, ?)''', (editionID, personID))

	if (p.partiture == True):
		partiture = 'Y'
	else:
		partiture = 'N'
	cur.execute('''insert into print (id, partiture, edition) values (?, ?, ?)''', (p.print_id, partiture, str(editionID)))
	print("Print " + str(p.print_id) + " is OK!")

conn.commit()
