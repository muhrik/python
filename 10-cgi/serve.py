#!/usr/bin/env python
import sys
import re
import numpy as np
import pandas as pd
import json
import http.client
import http.server
from aiohttp import web

if (len(sys.argv) == 1):
	print("The first command line argument must be a port number.")
	print("E.g. 9001")
	sys.exit()

if (len(sys.argv) == 2):
	print("The second command line argument must be a dir, whatever that is.")
	print("E.g. \"dir\"")
	sys.exit()
		
