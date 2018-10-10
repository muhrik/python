#!/usr/bin/env python
import sys

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
    print("Composer: " + str(self.edition.composition.authors))
    print("Title: " + str(self.edition.composition.name))
    print("Genre: " + str(self.edition.composition.genre))
    print("Key: " + str(self.edition.composition.key))
    print("Composition Year: " + str(self.edition.composition.year))
    #TODO print("Publication Year: " + str(self.edition.composition.Pubyear)) #TODO 
    print("Edition: " + str(self.edition.name))
    print("Editor: " + str(self.edition.authors))
    for k, v in self.edition.composition.voices:
      print("Voice " + str(k) + ": " + str(v))
    print("Partiture: " + str(self.partiture))
    print("Incipit: " + str(self.edition.composition.incipit)) 
  def composition():
    return edition.composition

class Voice:
  def __init__(self, name, range):
    self.name = name
    self.range = range

class Edition:
  def __init__(self, composition, authors, name):
    self.composition = composition
    self.authors = authors
    self.name = name

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

	composerDict = {}
	titleDict = {}
	genreDict = {}
	keyDict = {}
	compositionYearDict = {}
	publicationYearDict = {}
	editionDict = {}
	editorDict = {}
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
			for i in range(0, len(s)):
				composerDict[printNumber][i] = s[i].strip()
				composerDict[printNumber][i] = re.sub("[(].*[0-9].*[)]", "", composerDict[printNumber][i]).strip()
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
	if (m == None):
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

