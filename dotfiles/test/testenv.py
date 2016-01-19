#!/usr/bin/python

import os

import env

def setUp():
  env.homeDir = 'home/'
  env.inputFilesDir = 'inputfiles/'
  env.outputFilesDir = 'outputfiles/'
  setUpDirs()

def setUpDirs():
  for dir in [env.homeDir, env.inputFilesDir, env.outputFilesDir]:
    if not os.path.exists(dir):
      os.mkdir(dir)

def tearDown():
  for dir in [env.homeDir, env.inputFilesDir, env.outputFilesDir]:
    if os.path.exists(dir):
      os.rmdir(dir)
