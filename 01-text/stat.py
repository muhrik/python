#!/usr/bin/env python
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

if (len(sys.argv) == 1):
	print("The first command line argument must be a text file for the script to read.")
	print("E.g. scorelib.txt")
	sys.exit()
if (len(sys.argv) == 2):
	print("The second command line argument must be either \'composer\' or \'century\'.")
	print("No second command line argument has been received.")
	sys.exit()
file = open(sys.argv[1], 'r')

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

if (sys.argv[2] == "composer"):
	composerCountDict = {}
	for k, v in composerDict.items():
		for k2, v2 in v.items():
			if (composerCountDict.get(v2) == None):
				composerCountDict[v2] = 1
			else:
				composerCountDict[v2] = composerCountDict[v2] + 1
	for k, v in composerCountDict.items():
		print(k + ": " + str(v))

if (sys.argv[2] == "century"):
	centCountDict = {}
	for cntr in range(16,22):
		centCountDict[cntr] = 0;
		minYear = (cntr - 1) * 100
		maxYear = (cntr) * 100
		for k, v in compositionYearDict.items():
			if (v.isdigit()):
				year = int(v)
				if (year <= maxYear and year > minYear):
					centCountDict[cntr] = centCountDict[cntr] + 1
				if (year == cntr):
					centCountDict[cntr] = centCountDict[cntr] + 1
	for k, v in centCountDict.items():
		if (k <= 20):
			print(str(k) + "th century: " + str(v))
		if (k == 21):
			print(str(k) + "st century: " + str(v))
