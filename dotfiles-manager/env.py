#!/usr/bin/python

import os

from constants import Misc

home = os.environ['HOME'] + '/'
platform = ''
inputDir = ''
outputDir = home
backupsDir = ''
isGnu = ''
configFile = home + Misc.CONFIG_FILE.value