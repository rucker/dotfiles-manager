#!/usr/bin/python

import sys
import platform
import io
import os
from constants import Systems, BashInputFiles
import bashfile
import env

def init():
  identifySystem()

  env.homeDir = os.path.expanduser('~') + '/'
  env.workingDir = os.path.dirname(os.path.abspath(__file__)) + '/'
  env.inputFilesDir = env.workingDir + 'inputfiles/'
  env.outputFilesDir = env.workingDir[:env.workingDir.rfind('dotfiles/')]

  print "Environment:"
  print os.path.realpath(__file__)
  print "homeDir: " + env.homeDir
  print "workingDir: " + env.workingDir
  print "inputFilesDir: " + env.inputFilesDir
  print "outputFilesDir: " + env.outputFilesDir

  os.chdir(env.workingDir)

def identifySystem():
  supportedPlatforms = [Systems.DARWIN.value, Systems.LINUX.value]
  env.sysName = platform.system()

  if env.sysName not in supportedPlatforms:
    print "System not supported!"
    exit(1)
  print "System identified as " + env.sysName

if __name__ == '__main__':
  init()
  bashfile.compileBashProfile()
