#!/usr/bin/env python
import sys
import numpy
import re

if (len(sys.argv) == 1):
	print("The first command line argument must be a file with human-readable equations.")
	print("E.g. \"input.txt\"")
	sys.exit()

coeffRE = re.compile(r"[-+]?\s*[0-9]*[a-z]")
varRE = re.compile(r"[a-z]")
numRE = re.compile(r"[-+]?\s*[0-9]+")
equalsRE = re.compile(r"[=]\s*[-+]?[0-9]+")
signRE = re.compile(r"[-+]")

file = open(sys.argv[1], 'r')

coeffsMap = {}
equalMap = []
varOrdering = {}

index = 0
varIndex = 0
for line in file:
	coeffMap = {}
	for coeffStr in re.findall(coeffRE, line):
		numList = re.findall(numRE, coeffStr)
		if (numList == None or len(numList) == 0):
			#No number provided, assuming 1. Positive or negative ?
			signList = re.findall(signRE, coeffStr)
			if (signList == None or len(signList) == 0):
				#No sign, assuming positive
				coeff = 1
			else:
				if (signList[0] == "+"):
					coeff = 1
				if (signList[0] == "-"):
					coeff = -1
		else:
			coeff = int(numList[0])
		var = re.findall(varRE, coeffStr)[0]
		if (varOrdering.get(var) == None):
			varOrdering[var] = varIndex
			varIndex = varIndex + 1
		coeffMap[var] = coeff
	coeffsMap[index] = coeffMap
	for equalsStr in re.findall(equalsRE, line):
		numStr = equalsStr.replace("=", "")
		equalMap.insert(index, int(numStr))
	index = index + 1
numEquations = index


aPy = []
for lineIndex, coeffMap in coeffsMap.items():
	aPyElem = []
	for var, k in varOrdering.items():
		aPyElem.append(0)
	for var, coeff in coeffMap.items():
		varIndex = varOrdering[var]
		aPyElem[varIndex] = coeff
	aPy.append(aPyElem)

#print("CoeffsMap and equalMap")
#print(str(coeffsMap))
#print("")
#print(str(equalMap))
#print("")
#print("")

#print("aPy and equalMap")
#print(str(aPy))
#print("")
#print(str(equalMap))
#print("")
#print("")

a = numpy.asarray(aPy)
b = numpy.asarray(equalMap)

#print("a and b")
#print(str(a))
#print("")
#print(str(b))
#print("")
#print("")

aRank = numpy.linalg.linalg.matrix_rank(a) #Get original matrix rank

aAugmented = numpy.column_stack((a,b))
aAugmentedRank = numpy.linalg.matrix_rank(aAugmented) #Get augmented Matrix rank

if (aAugmentedRank > aRank): #If the rank of the augmented matrix is greater than the rank of the original matrix, the system has no solution.
	print("No solution")
	sys.exit()	

if (aRank < numEquations and aAugmentedRank == aRank):
	print("Solution space dimension: " + str(numEquations - aRank))
	sys.exit()

solution = numpy.linalg.solve(a, b)
#print("solution")
#print(str(solution))

printStr = "Solution: "
for var, varIndex in varOrdering.items():
	printStr = printStr + var + "=" + str(solution[varIndex]) + " "

print(printStr)
