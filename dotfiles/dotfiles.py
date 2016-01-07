#!/usr/bin/python

import sys
import platform
import io
import os
from constants import Systems, VimFiles
import bashfile
import env

def init():
  identifySystem()

  env.homeDir = os.path.expanduser('~') + '/'
  env.workingDir = os.path.dirname(os.path.abspath(__file__)) + '/'
  env.inputFilesDir = env.workingDir + 'inputfiles/'
  env.outputFilesDir = env.workingDir[:env.workingDir.rfind('dotfiles/')]

  print "Environment:"
  print "\tplatform: " + env.platform
  print "\thomeDir: " + env.homeDir
  print "\tworkingDir: " + env.workingDir
  print "\tinputFilesDir: " + env.inputFilesDir
  print "\toutputFilesDir: " + env.outputFilesDir

  os.chdir(env.workingDir)

def identifySystem():
  supportedPlatforms = [Systems.DARWIN.value, Systems.LINUX.value]
  env.platform = platform.system()

  if env.platform not in supportedPlatforms:
    print "System not supported!"
    exit(1)

def symlink(targetName, linkName) :
  target = env.outputFilesDir + targetName
  link = env.homeDir + linkName
  print "Symlink " + link + " -> " + target
  if os.path.islink(link):
      print "\tLink already exists."
      return
  elif os.path.isfile(link):
      print "\tRegular file exists at " + link + ". Renaming to " + linkName + ".bak"
      os.rename(link, link + ".bak")
  else:
    print "\tSymlink does not exist."
  print "Creating..."
  os.symlink(target, link)
  print "\tLink created."

def main():
  print "\nPreparing dotfiles!\n"
  init()
  bashfile.compileBashFiles()
  symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
  print "\nDone."

if __name__ == '__main__':
  main()
