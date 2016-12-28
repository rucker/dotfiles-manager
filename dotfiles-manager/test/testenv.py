#!/usr/bin/python

import os
import shutil
import tempfile
import argparse

import testfilemocks
from constants import Misc

tmp = tempfile.gettempdir() + '/'
inputDir = tmp + 'testsrc/'
outputDir = tmp + 'testoutputfiles/'
backupsDir = tmp + 'testbackups/'
scriptsDir = ''
configFile = tmp + Misc.CONFIG_FILE.value
parser = argparse.ArgumentParser()
args = ''

def setUp():
    setUpDirs()
    testfilemocks.createInputFiles()

def setUpDirs():
    for dir in [inputDir, outputDir, backupsDir]:
        if not os.path.exists(dir):
            os.mkdir(dir)
    testfilemocks.createFile(configFile, 'inputDir=' + inputDir)

def clearArgs():
    args = parser.parse_args([])

def tearDown():
    for dir in [inputDir, outputDir, backupsDir]:
        if tmp not in dir:
            abort()
        if os.path.exists(dir):
            shutil.rmtree(dir)
    if tmp not in configFile:
        abort()
    if os.path.isfile(configFile):
        os.remove(configFile)

def abort():
    print "A test attempted to tear down the directory ", dir, "! Please check test set-up and be sure to use the testenv temp dir, ", tmp
    exit(1)
