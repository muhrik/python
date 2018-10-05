import sys
import re

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

file = open('scorelib.txt', 'r')

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
			printNumber = m.group(1)
	if (m == None):
		m = composerRE.match(line)
		if (m != None):
			composerDict[printNumber] = m.group(1)
	if (m == None):
		m = titleRE.match(line)
		if (m != None):
			titleDict[printNumber] = m.group(1)
	if (m == None):
		m = genreRE.match(line)
		if (m != None):
			genreDict[printNumber] = m.group(1)
	if (m == None):
		m = keyRE.match(line)
		if (m != None):
			keyDict[printNumber] = m.group(1)
	if (m == None):
		m = CompositionYearRE.match(line)
		if (m != None):
			compositionYearDict[printNumber] = m.group(1)
	if (m == None):
		m = PublicationYearRE.match(line)
		if (m != None):
			publicationYearDict[printNumber] = m.group(1)
	if (m == None):
		m = EditionRE.match(line)
		if (m != None):
			editionDict[printNumber] = m.group(1)
	if (m == None):
		m = EditorRE.match(line)
		if (m != None):
			editorDict[printNumber] = m.group(1)
	if (m == None):
		m = VoiceRE.match(line)
		if (m != None):
			s = m.group(1).split(":")
			if (s[0] == "1"):
				voiceDict[printNumber] = {}
			voiceDict[printNumber][s[0]] = s[1]
	if (m == None):
		m = PartitureRE.match(line)
		if (m != None):
			partitureDict[printNumber] = m.group(1)
	if (m == None):
		m = IncipitRE.match(line)
		if (m != None):
			incipitDict[printNumber] = m.group(1)
