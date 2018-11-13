#!/usr/bin/env python
import sys
import re
import numpy as np
import pandas as pd
import json
from scipy import stats
import collections

if (len(sys.argv) == 1):
	print("The first command line argument must be a csv file with student data.")
	print("E.g. \"points.csv\"")
	sys.exit()

if (len(sys.argv) == 2):
	print("The second command line argument must be either a number or \"average\".")
	sys.exit()
		
df = pd.read_csv(sys.argv[1])
columnNames = list(df)

dataMap = {}
# Get values for each deadline - regardless whether the student is "average" or chosen via ID.
if (sys.argv[2] == "average"):
	for columnName in columnNames:
		if (columnName == "student"):
			continue
		exercise = re.sub(r"[0-9][0-9][0-9][0-9][-][0-9][0-9][-][0-9][0-9]", "", columnName)
		exerciseNum = re.sub(r"[/]", "", exercise)

		dataMap[exerciseNum] = df.filter(like=exercise).mean().mean()
else:
	for index, row in df.iterrows():
		if (int(row["student"]) == int(sys.argv[2])):
			for columnName in columnNames:
				if (columnName == "student"):
					continue
				exercise = re.sub(r"[0-9][0-9][0-9][0-9][-][0-9][0-9][-][0-9][0-9]", "", columnName)
				exerciseNum = re.sub(r"[/]", "", exercise)
				if (dataMap.get(exerciseNum) == None or int(dataMap[exerciseNum]) == 0):
					dataMap[exerciseNum] = row[columnName]

dataMapOrdered = collections.OrderedDict(sorted(dataMap.items()))
npArray = np.asarray(list(dataMapOrdered.values()), dtype=np.float64);

mean = np.average(npArray)
median = np.median(npArray)
positiveValues = npArray[npArray > 0]
passed = len(positiveValues)
total = np.sum(npArray)
npCumSumArray = np.cumsum(npArray)
npTimeArray = np.asarray(list(range(0, len(npArray))), dtype=np.float64)
slope = stats.linregress(npTimeArray, npCumSumArray).slope
gainPerDay = slope / 7.0
#TODO: expected number of days until 16 and 20 points. JSON output, use dumps just like in stat.py.

