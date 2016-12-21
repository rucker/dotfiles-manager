#!/usr/bin/python

import os
import shutil

import env
import testfilemocks

def setUp():
    thisDir = os.path.dirname(os.path.realpath(__file__)) + '/'
    env.inputFilesDir = thisDir + 'testinputfiles/'
    env.outputFilesDir = thisDir + 'testoutputfiles/'
    env.backupsDir = thisDir + 'testbackups/'
    setUpDirs()
    testfilemocks.createInputFiles()

def setUpDirs():
    for dir in [env.outputFilesDir, env.inputFilesDir, env.outputFilesDir, env.backupsDir]:
        if not os.path.exists(dir):
            os.mkdir(dir)

def clearArgs():
    env.args = env.parser.parse_args([])

def tearDown():
    for dir in [env.inputFilesDir, env.outputFilesDir, env.backupsDir]:
        if os.path.exists(dir):
            shutil.rmtree(dir)
