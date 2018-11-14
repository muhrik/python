#!/usr/bin/env python
import sys
import re
import numpy as np
import pandas as pd
import json
from scipy import stats
import collections
import datetime

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
if (slope == 0):
	date16 = "inf"
	date20 = "inf"
else:
	daysUntil16 = (16 - total) / gainPerDay
	daysUntil20 = (20 - total) / gainPerDay
	date16 = datetime.datetime.now() #Assumes the data is current
	date20 = datetime.datetime.now() #Assumes the data is current
	for i in range(0, int(daysUntil16) + 1): 
	    date16 += datetime.timedelta(days=1)
	for i in range(0, int(daysUntil20) + 1): 
	    date20 += datetime.timedelta(days=1)
	date16 = date16.date()
	date20 = date20.date()

outputMap = {}
outputMap["mean"] = mean
outputMap["median"] = median
outputMap["total"] = total
outputMap["passed"] = passed
outputMap["regression slope"] = gainPerDay
outputMap["date 16"] = str(date16)
outputMap["date 20"] = str(date20)

print(json.dumps(outputMap, sort_keys=True, indent=4, separators=(',', ': ')))
