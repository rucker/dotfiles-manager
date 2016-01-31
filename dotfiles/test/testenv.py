#!/usr/bin/python

import os
import shutil
import argparse

import env
import testfilemocks

def setUp():
  thisDir = os.path.dirname(os.path.realpath(__file__)) + '/'
  env.homeDir = thisDir + 'testhome/'
  env.inputFilesDir = thisDir + 'testinputfiles/'
  env.outputFilesDir = thisDir + 'testoutputfiles/'
  setUpDirs()
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clobber', action='store_true')
  env.args = parser.parse_args(['-c'])
  testfilemocks.createInputFiles()

def setUpDirs():
  for dir in [env.homeDir, env.inputFilesDir, env.outputFilesDir]:
    if not os.path.exists(dir):
      os.mkdir(dir)

def tearDown():
  for dir in [env.homeDir, env.inputFilesDir, env.outputFilesDir]:
    if os.path.exists(dir):
      shutil.rmtree(dir)
