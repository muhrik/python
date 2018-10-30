#!/usr/bin/env python
import sys
import numpy
import re
import wave
import struct

if (len(sys.argv) == 1):
	print("The first command line argument must be a .wav file, PCM, sample rate 8-48 kHz.")
	print("E.g. \"input.txt\"")
	sys.exit()

nums = []
index = 0

file = wave.open(sys.argv[1])
numFrames = file.getnframes()

for i in range(1, numFrames):
	string = file.readframes(1)
	tuple = struct.unpack("<H", string)

	for num in tuple:
		nums[index] = num
		index = index + 1

a = numpy.asarray(nums)
output = numpy.fft.rfft(a)
absOutput = numpy.absolute(output)

absOutputAverage = numpy.average(absOutput)[0]
absOutputAverageTwenty = absOutputAverage * 20

peaks = {}
for i in range(0, len(absOutput) - 1):
	cn = absOutput[i]
	if (cn >= absOutputAverageTwenty):
		peaks[i] = cn

	



