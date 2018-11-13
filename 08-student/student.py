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

