#!/usr/bin/env python
import sys
import numpy
import re
import wave
import struct

if (len(sys.argv) == 1):
	print("The first command line argument must be a number representing audio frequency.")
	print("E.g. \"440\"")
	sys.exit()

if (len(sys.argv) == 2):
	print("The second command line argument must be a .wav file, PCM, sample rate 8-48 kHz.")
	print("E.g. \"sample.wav\"")
	sys.exit()

octaveMap = {}
basePitch = sys.argv[1]
octaveMap["A,,"] = octaveMap / 16
octaveMap["A,"] = octaveMap / 8
octaveMap["A"] = octaveMap / 4
octaveMap["a"] = octaveMap / 2
octaveMap["a'"] = octaveMap
octaveMap["a''"] = octaveMap * 2

pitchNames = {}
pitchNames[1] = "c"
pitchNames[2] = "cis"
pitchNames[3] = "d"
pitchNames[4] = "es"
pitchNames[5] = "e"
pitchNames[6] = "f"
pitchNames[7] = "fis"
pitchNames[8] = "g"
pitchNames[9] = "gis"
pitchNames[10] = "a"
pitchNames[11] = "bes"
pitchNames[12] = "b"

