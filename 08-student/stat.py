#!/usr/bin/env python
import sys
import numpy
import pandas as pd

if (len(sys.argv) == 1):
	print("The first command line argument must be a csv file with student data.")
	print("E.g. \"points.csv\"")
	sys.exit()

if (len(sys.argv) == 2):
	print("The second command line argument must be either \"dates\", \"deadlines\", or \"exercises\".")
	sys.exit()
		
df = pd.read_csv(sys.argv[1])
columnNames = list(df)


meanMap = {}
medianMap = {}
firstQMap = {}
secondQMap = {}
if (sys.argv[2] == "dates"):
	for columnName in columnNames:
		if (columnName == "student"):
			continue:
		mean = df[columnName].mean()
		median = df[columnName].median()
		firstQ = df[columnName].quantile(0.25)
		lastQ = df[columnName].quantile(0.75)
if (sys.argv[2] == "deadlines"):

if (sys.argv[2] == "exercises"):



#studentMap = {} # student data submaps mapped onto their IDs
#for index, row in df.iterrows():
#	studentDataMap = {} # student data submaps where their data is mapped onto their keys
#	studentID = 0
#	for columnName in columnNames:
#		if (columnName == "student"):
#			studentID = row[columnName]
#			continue
#		studentDataMap[columnName] = row[columnName]
#	studentMap[studentID] = studentDataMap

