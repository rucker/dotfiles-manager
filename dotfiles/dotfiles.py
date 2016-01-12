#!/usr/bin/python

import sys
import platform
import io
import os
from constants import Systems, VimFiles
import bashfile
import gitconfig
import env

def init():
  identifySystem()

  env.homeDir = os.path.expanduser('~') + '/'
  env.homeBinDir = env.homeDir + 'bin/'
  env.workingDir = os.path.dirname(os.path.realpath(__file__)) + '/'
  env.inputFilesDir = env.workingDir + 'inputfiles/'
  env.scriptsDir = env.workingDir + 'scripts/'
  env.outputFilesDir = env.workingDir[:env.workingDir.rfind('dotfiles/')]

  print "Environment:"
  print "\tplatform: " + env.platform
  print "\thomeDir: " + env.homeDir
  print "\thomeBinDir: " + env.homeBinDir
  print "\tworkingDir: " + env.workingDir
  print "\tinputFilesDir: " + env.inputFilesDir
  print "\tscriptsDir: " + env.scriptsDir
  print "\toutputFilesDir: " + env.outputFilesDir
  print ""

  os.chdir(env.workingDir)

def identifySystem():
  supportedPlatforms = [Systems.DARWIN.value, Systems.LINUX.value]
  env.platform = platform.system()

  if env.platform not in supportedPlatforms:
    print "System not supported!"
    exit(1)

def symlink(target, linkName) :
  print "Symlink " + linkName + " -> " + target
  if os.path.islink(linkName):
      print "\tLink already exists.\n"
      return
  elif os.path.isfile(linkName):
      print "\tRegular file exists at " + linkName + ". Renaming to " + linkName + ".bak"
      os.rename(linkName, linkName + ".bak")
  else:
    print "\tSymlink does not exist."
  print "\tCreating..."
  os.symlink(target, linkName)
  print "\tLink created.\n"

def promptForDirCreation(dirPath):
  shouldCreateDir = ''
  while shouldCreateDir not in ['Y','N']:
    print "ATTENTION: " + dirPath + " does not exist."
    shouldCreateDir = raw_input("Would you like to create it? (Y/N): ").upper()
    if shouldCreateDir == 'Y':
      print "Creating dir " + dirPath + "...\n"
      os.makedirs(dirPath)
      return True
    else:
      print "Skipping...\n"
      return False

def createSymlinks():
  symlink(env.outputFilesDir + VimFiles.VIMRC.value, env.homeDir + VimFiles.DOT_VIMRC.value)
  if not os.path.exists(env.homeBinDir):
    if not promptForDirCreation(env.homeBinDir):
      return
  symlink(os.path.realpath(__file__), env.homeBinDir + 'dotfiles')

def main():
  print "\nPreparing dotfiles!\n"
  init()
  bashfile.compileBashFiles()
  gitconfig.compileGitConfig()
  createSymlinks()
  print "Done."

if __name__ == '__main__':
  main()
