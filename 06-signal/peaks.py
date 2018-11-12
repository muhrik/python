#!/usr/bin/env python
#author: Mario Uhrik 433501
import sys
import numpy as np
import wave
import struct

if (len(sys.argv) == 1):
	print("The first command line argument must be a .wav file, PCM, sample rate 8-48 kHz.")
	print("E.g. \"sample.wav\"")
	sys.exit()

file = wave.open(sys.argv[1])
numFrames = file.getnframes()
numChannels = file.getnchannels()
numSamples = numFrames * numChannels
frameRate = file.getframerate()
data = file.readframes(numFrames)
file.close()

nums = struct.unpack("%ih" % numSamples, data)

minPeakIndex = -1
maxPeakIndex = -1

for windowIndex in range(0, len(nums) / (frameRate*numChannels) ):
	windowNumsIndexLeft = windowIndex * frameRate*numChannels
	windowNumsIndexRight = windowNumsIndexLeft + frameRate*numChannels
	windowNums = nums[windowNumsIndexLeft:windowNumsIndexRight]
	a = np.asarray(windowNums)
	
	if (numChannels == 2):
		left = a[::2]
		right = a[1::2]
		wAverage = (left + right) / 2
		out = np.fft.rfft(wAverage)
	if (numChannels == 1):
		out = np.fft.rfft(a)
	absOut = np.absolute(out)

	absOutAverage = np.average(absOut)
	absOutAverageTwenty = absOutAverage * 20

	for i in range(0, len(absOut)):
		cn = absOut[i]
		if (cn >= absOutAverageTwenty):
			if (minPeakIndex == -1):
				minPeakIndex = i
			maxPeakIndex = i


if (minPeakIndex == -1 and maxPeakIndex == -1):
	print("no peaks")
else:
	print("low = " + str(minPeakIndex) + ", high = " + str(maxPeakIndex))

