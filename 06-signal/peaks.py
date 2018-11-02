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

file = wave.open(sys.argv[1])
numFrames = file.getnframes()
numChannels = file.getnchannels()
numSamples = numFrames * numChannels

data = file.readframes(numFrames)

nums = struct.unpack("%ih" % numSamples, data)

#for num in nums: #DEBUG
#	print("Num " + str(num)) #DEBUG

a = numpy.asarray(nums)
output = numpy.fft.rfft(a)
absOutput = numpy.absolute(output)

absOutputAverage = numpy.average(absOutput)
absOutputAverageTwenty = absOutputAverage * 20

minPeak = -1
maxPeak = -1
for i in range(0, len(absOutput) - 1):
	cn = absOutput[i]
	#print("Iteration " + str(i) + ": " + str(cn)) #DEBUG
	if (cn >= absOutputAverageTwenty):
		if (minPeak == -1 and maxPeak == -1):
			minPeak = cn
			maxPeak = cn
		if (minPeak > cn):
			minPeak = cn
		if (maxPeak < cn):
			maxPeak = cn

if (minPeak == -1 and maxPeak == -1):
	print("no peaks")
else:
	print("low = " + str(minPeak) + ", high = " + str(maxPeak))
#print("AVG: " + str(absOutputAverage)) #DEBUG
#print("AVG20: " + str(absOutputAverageTwenty)) #DEBUG


