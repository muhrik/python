#!/usr/bin/env python
import sys
import numpy
import re

if (len(sys.argv) == 1):
	print("The first command line argument must be a file with human-readable equations.")
	print("E.g. \"input.txt\"")
	sys.exit()

coeffRE = re.compile(r"[-+]?[0-9]+[a-z]")
varRE = re.compile(r"[a-z]")
equalsRE = re.compile(r"=[.]*[-+]?[0-9]+")

file = open(sys.argv[1], 'r')

coeffsMap = {}
equalMap = {}

index = 0
for line in file:
	coeffMap = {}
	for coeffStr in re.findall(coeffRE, line):
		coeff = int(coeffStr)
		var = re.findall(varRE, coeffStr)[0]
		coeffMap[var] = coeff
	coeffsMap[index] = coeffMap	
	for equalsStr in re.findall(equalsRE, line):
		numStr = equalsStr.replace("=", "")
		equalMap[index] = int(numStr)
	index = index + 1

#TODO: The above should be working code to parse the file. Now just create arrays and give them to numpy.

#TODO: If the equation system is full-rank, then solve the equations, otherwise return something related to their rank
#https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.linalg.solve.html
#numpy.linalg.solve(a, b)
