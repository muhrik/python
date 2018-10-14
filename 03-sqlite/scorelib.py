#!/usr/bin/env python
import sys
import re

class Person:
  def __init__(self, name, born, died):
    self.name = name
    self.born = born
    self.died = died
  def greet( self ):
    print( "hello " + self.name )

class Print:
  def __init__(self, edition, print_id, partiture):
    self.edition = edition
    self.print_id = print_id
    self.partiture = partiture
  def format(self):
    print("Print Number: " + str(self.print_id))
    sys.stdout.write("Composer: ")
    for i in range(0, len(self.edition.composition.authors)):
      sys.stdout.write((self.edition.composition.authors[i].name))
      if (self.edition.composition.authors[i].born != None and self.edition.composition.authors[i].died != None):
        sys.stdout.write(" (" + str(self.edition.composition.authors[i].born) + "--" + str(self.edition.composition.authors[i].died) + ")")
      if (self.edition.composition.authors[i].born != None and self.edition.composition.authors[i].died == None):
        sys.stdout.write(" (" + str(self.edition.composition.authors[i].born) + ")")
      if (i == len(self.edition.composition.authors) - 1):
        sys.stdout.write("\n")
      else:
        sys.stdout.write(";")

    print("Title: " + str(self.edition.composition.name))
    print("Genre: " + str(self.edition.composition.genre))
    print("Key: " + str(self.edition.composition.key))
    sys.stdout.write("Composition Year: ")
    if (self.edition.composition.year == None):
      sys.stdout.write("\n")
    else:
      sys.stdout.write(str(self.edition.composition.year) + "\n")
    sys.stdout.write("Publication Year: ")
    if (self.edition.year == None):
      sys.stdout.write("\n")
    else:
      sys.stdout.write(str(self.edition.year) + "\n")
    print("Edition: " + str(self.edition.name))
    print("Editor: " + str(self.edition.authors[0].name))
    iter = 0
    for v in self.edition.composition.voices:
      print("Voice " + str(iter + 1) + ": " + v.name)
      iter = iter + 1
    if (self.partiture == True):
      print("Partiture: " + "yes")
    else:
      print("Partiture: " + "no")
    print("Incipit: " + str(self.edition.composition.incipit)) 
  def composition():
    return edition.composition

class Voice:
  def __init__(self, name, range):
    self.name = name
    self.range = range

class Edition:
  def __init__(self, composition, authors, name, year):
    self.composition = composition
    self.authors = authors
    self.name = name
    self.year = year

class Composition:
  def __init__(self, name, incipit, key, genre, year, voices, authors):
    self.name = name
    self.incipit = incipit
    self.key = key
    self.genre = genre
    self.year = year
    self.voices = voices
    self.authors = authors

def load(filename):
	file = open(filename, 'r')

	printNumberRE = re.compile(r"Print Number: (.*)")
	composerRE = re.compile(r"Composer: (.*)")
	titleRE = re.compile(r"Title: (.*)")
	genreRE = re.compile(r"Genre: (.*)")
	keyRE = re.compile(r"Key: (.*)")
	CompositionYearRE = re.compile(r"Composition Year: (.*)")
	PublicationYearRE = re.compile(r"Publication Year: (.*)")
	EditionRE = re.compile(r"Edition: (.*)")
	EditorRE = re.compile(r"Editor: (.*)")
	VoiceRE = re.compile(r"Voice (.*)")
	PartitureRE = re.compile(r"Partiture: (.*)")
	IncipitRE = re.compile(r"Incipit: (.*)")


	composerDict = {}
	composerBornDict = {}
	composerDiedDict = {}
	titleDict = {}
	genreDict = {}
	keyDict = {}
	compositionYearDict = {}
	publicationYearDict = {}
	editionDict = {}
	editorDict = {}
	editorBornDict = {}
	editorDiedDict = {}
	voiceDict = {}
	partitureDict = {}
	incipitDict = {}

	for line in file:
		m = None
		if (m == None):
			m = printNumberRE.match(line)
			if (m != None):
				printNumber = m.group(1).strip()
		if (m == None):
			m = composerRE.match(line)
			if (m != None):
				s = m.group(1).strip().split(";")
				composerDict[printNumber] = {}
				composerBornDict[printNumber] = {}
				composerDiedDict[printNumber] = {}
				for i in range(0, len(s)):
					composerDict[printNumber][i] = s[i].strip()
					rnge = re.search("[(][1-3][0-9]{3}[-]*[1-3][0-9]{3}[)]", composerDict[printNumber][i])
					if (rnge != None):
						bornYear = re.search("[1-3][0-9]{3}", composerDict[printNumber][i]).group(0).strip()
						diedYear = re.search("[-][1-3][0-9]{3}", composerDict[printNumber][i]).group(0).strip()
						diedYear = re.search("[1-3][0-9]{3}", diedYear).group(0).strip()
						composerBornDict[printNumber][i] = bornYear
						composerDiedDict[printNumber][i] = diedYear
						composerDict[printNumber][i] = re.sub("[(][1-3][0-9]{3}[-]*[1-3][0-9]{3}[)]", "", composerDict[printNumber][i]).strip()
					brn = re.search("[(][1-3][0-9]{3}.*[)]", composerDict[printNumber][i])
					if (brn != None):
						bornYear = re.search("[1-3][0-9]{3}", composerDict[printNumber][i]).group(0).strip()
						composerBornDict[printNumber][i] = bornYear
						composerDict[printNumber][i] = re.sub("[(][1-3][0-9]{3}.*[)]", "", composerDict[printNumber][i]).strip()
		if (m == None):
			m = titleRE.match(line)
			if (m != None):
				titleDict[printNumber] = m.group(1).strip()
		if (m == None):
			m = genreRE.match(line)
			if (m != None):
				genreDict[printNumber] = m.group(1).strip()
		if (m == None):
			m = keyRE.match(line)
			if (m != None):
				keyDict[printNumber] = m.group(1).strip()
		if (m == None):
			m = CompositionYearRE.match(line)
			if (m != None):
				year = re.search("[1-3][0-9]{3}", m.group(1))
				if (year != None):
					compositionYearDict[printNumber] = year.group(0).strip()
				else:
					century = re.search("[1][0-9][t][h]", m.group(1))
					if (century != None):
						compositionYearDict[printNumber] = century.group(0).strip().strip("th").strip()
		if (m == None):
			m = PublicationYearRE.match(line)
			if (m != None):
				year = re.search("[1-3][0-9]{3}", m.group(1))
				if (year != None):
					publicationYearDict[printNumber] = year.group(0).strip()
		if (m == None):
			m = EditionRE.match(line)
			if (m != None):
				editionDict[printNumber] = m.group(1).strip()
		if (m == None): #TODO - parse born
			m = EditorRE.match(line)
			if (m != None):
				editorDict[printNumber] = m.group(1).strip()
		if (m == None):
			m = VoiceRE.match(line)
			if (m != None):
				s = m.group(1).strip().split(":")
				if (s[0] == "1"):
					voiceDict[printNumber] = {}
				voiceDict[printNumber][s[0]] = s[1].strip()
		if (m == None):
			m = PartitureRE.match(line)
			if (m != None):
				partitureDict[printNumber] = m.group(1).strip()
		if (m == None):
			m = IncipitRE.match(line)
			if (m != None):
				incipitDict[printNumber] = m.group(1).strip()

	prints = []
	
	for k, v in titleDict.items():
		name_C = titleDict.get(k)
		incipit = incipitDict.get(k)
		key = keyDict.get(k)
		genre = genreDict.get(k)
		year = compositionYearDict.get(k)
		if (year != None):
			year = int(year)
		voices = []
		year_E = publicationYearDict.get(k)
		for kVoice, vVoice in voiceDict.get(k).items():
			voice = Voice(vVoice, None)
			voices.append(voice)
		authors_C = []
		for kAuthor, vAuthor in composerDict.get(k).items():
			born = composerBornDict.get(k).get(kAuthor)
			if (born != None):
				born = int(born)
			died = composerDiedDict.get(k).get(kAuthor)
			if (died != None):
				died = int(died)
			author = Person(vAuthor, born, died)
			authors_C.append(author)
		#TODO
		#authors_E = []
		#for kEditor, vEditor in editorDict.get(k).items():
		#	editor = Person(vEditor, None, None)
		#	authors_E.append(editor)
		authors_E = []
		editor = Person(editorDict.get(k), None, None)
		authors_E.append(editor)
		name_E = editionDict.get(k)
		partiture = partitureDict.get(k)
		if (partiture == "yes"):
			partitureBool = True
		if (partiture == "no"):
			partitureBool = False

		co = Composition(name_C, incipit, key, genre, year, voices, authors_C)
		ed = Edition(co, authors_E, name_E, year_E)
		pr = Print(ed, int(k), partitureBool)
		prints.append(pr)

	prints.sort(key=sorter)
	return prints

def sorter(elem):
	return elem.print_id
