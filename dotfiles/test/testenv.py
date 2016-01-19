#!/usr/bin/python

import os
import shutil

import env

def setUp():
  env.homeDir = 'testhome/'
  env.inputFilesDir = 'testinputfiles/'
  env.outputFilesDir = 'testoutputfiles/'
  setUpDirs()

def setUpDirs():
  for dir in [env.homeDir, env.inputFilesDir, env.outputFilesDir]:
    if not os.path.exists(dir):
      os.mkdir(dir)

def tearDown():
  for dir in [env.homeDir, env.inputFilesDir, env.outputFilesDir]:
    if os.path.exists(dir):
      shutil.rmtree(dir)
