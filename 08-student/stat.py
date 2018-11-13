#!/usr/bin/env python
import sys
import re
import numpy as np
import pandas as pd
import json

if (len(sys.argv) == 1):
	print("The first command line argument must be a csv file with student data.")
	print("E.g. \"points.csv\"")
	sys.exit()

if (len(sys.argv) == 2):
	print("The second command line argument must be either \"dates\", \"deadlines\", or \"exercises\".")
	sys.exit()
		
df = pd.read_csv(sys.argv[1])
columnNames = list(df)


dataMap = {}
if (sys.argv[2] == "dates"):
	for columnName in columnNames:
		if (columnName == "student"):
			continue
		date = 	re.sub(r"[/][0-9][0-9]", "", columnName)

		subDataMap = {}
		subDataMap["mean"] = df.filter(like=date).mean().mean()
		subDataMap["median"] = df.filter(like=date).median().median()
		subDataMap["first"] = df.filter(like=date).quantile(0.25).quantile(0.25)
		subDataMap["last"] = df.filter(like=date).quantile(0.75).quantile(0.75)
		subDataMap["passed"] = df.filter(like=date).pct_change().gt(0).sum().sum()

		dataMap[date] = subDataMap
if (sys.argv[2] == "deadlines"):
	for columnName in columnNames:
		if (columnName == "student"):
			continue

		subDataMap = {}
		subDataMap["mean"] = df[columnName].mean()
		subDataMap["median"] = df[columnName].median()
		subDataMap["first"] = df[columnName].quantile(0.25)
		subDataMap["last"] = df[columnName].quantile(0.75)
		subDataMap["passed"] = df[columnName].pct_change().gt(0).sum()

		dataMap[columnName] = subDataMap
if (sys.argv[2] == "exercises"):
	for columnName in columnNames:
		if (columnName == "student"):
			continue
		exercise = re.sub(r"[0-9][0-9][0-9][0-9][-][0-9][0-9][-][0-9][0-9]", "", columnName)
		exerciseNum = re.sub(r"[/]", "", exercise)

		subDataMap = {}
		subDataMap["mean"] = df.filter(like=exercise).mean().mean()
		subDataMap["median"] = df.filter(like=exercise).median().median()
		subDataMap["first"] = df.filter(like=exercise).quantile(0.25).quantile(0.25)
		subDataMap["last"] = df.filter(like=exercise).quantile(0.75).quantile(0.75)
		subDataMap["passed"] = df.filter(like=exercise).pct_change().gt(0).sum().sum()

		dataMap[exerciseNum] = subDataMap

print(json.dumps(dataMap, sort_keys=True, indent=4, separators=(',', ': ')))
