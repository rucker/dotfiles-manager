#!/usr/bin/python

import os
import shutil

import env
import testfilemocks

def setUp():
    thisDir = os.path.dirname(os.path.realpath(__file__)) + '/'
    env.srcDir = thisDir + 'testsrc/'
    env.outputDir = thisDir + 'testoutputfiles/'
    env.backupsDir = thisDir + 'testbackups/'
    setUpDirs()
    testfilemocks.createInputFiles()

def setUpDirs():
    for dir in [env.outputDir, env.srcDir, env.outputDir, env.backupsDir]:
        if not os.path.exists(dir):
            os.mkdir(dir)

def clearArgs():
    env.args = env.parser.parse_args([])

def tearDown():
    for dir in [env.srcDir, env.outputDir, env.backupsDir]:
        if os.path.exists(dir):
            shutil.rmtree(dir)
