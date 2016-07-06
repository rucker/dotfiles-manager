#!/usr/bin/python

import sys
import platform
import io
import os
import argparse

from constants import Systems, BashOutputFiles, VimFiles, GitConfigOutputFiles
import bashfile
import gitconfig
import env
import ioutils

def init():
  identifySystem()
  setArgs()
  setEnv()
  os.chdir(env.workingDir)

def identifySystem():
  supportedPlatforms = [Systems.DARWIN.value, Systems.LINUX.value]
  env.platform = platform.system()

  if env.platform not in supportedPlatforms:
    print "System not supported!"
    exit(1)

def setArgs():
  parser = argparse.ArgumentParser(description="Compile your custom dotfiles from input files.")
  parser.add_argument('-c', '--clobber', action='store_true', help="Clobber any existing output files (don't back them up).")
  parser.add_argument('-r', '--revert', action='store_true', help="Revert dotfiles to backed-up version.")
  env.args = parser.parse_args()
  print "\nPreparing dotfiles!\n"

def setEnv():
  env.homeDir = os.path.expanduser('~') + '/'
  env.workingDir = os.path.dirname(os.path.realpath(__file__)) + '/'
  env.inputFilesDir = env.workingDir + 'inputfiles/'
  env.scriptsDir = env.workingDir + 'scripts/'
  env.outputFilesDir = env.workingDir[:env.workingDir.rfind('dotfiles/')]

  print "Environment:"
  print "\tplatform: " + env.platform
  print "\thomeDir: " + env.homeDir
  print "\tworkingDir: " + env.workingDir
  print "\tinputFilesDir: " + env.inputFilesDir
  print "\tscriptsDir: " + env.scriptsDir
  print "\toutputFilesDir: " + env.outputFilesDir
  print "\targs: " + str(env.args)
  print ""

def symlink(target, linkName) :
  print "Symlink " + linkName + " -> " + target
  if os.path.islink(linkName):
    print "\tLink already exists.\n"
    return
  elif os.path.isfile(linkName):
    ioutils.backupFile(linkName)
  else:
    print "\tSymlink does not exist."
  print "\tCreating..."
  os.symlink(target, linkName)
  print "\tLink created.\n"

def createSymlinks():
  symlink(env.outputFilesDir + VimFiles.VIMRC.value, env.homeDir + VimFiles.DOT_VIMRC.value)

def cleanUp():
  ioutils.cleanUpRenamedFiles([ BashOutputFiles.DOT_BASH_PROFILE.value, BashOutputFiles.DOT_BASHRC.value, VimFiles.DOT_VIMRC.value, GitConfigOutputFiles.DOT_GITCONFIG.value ])

def printCompletionMessage():
  if env.platform == Systems.DARWIN.value:
    bashFileName = BashOutputFiles.DOT_BASH_PROFILE.value
  else:
    bashFileName = BashOutputFiles.DOT_BASHRC.value
  print "Done. Recommend you source ~/" + bashFileName + " or start new a terminal session."

def main():
  init()
  if env.args.revert:
    ioutils.revertDotFiles([ BashOutputFiles.DOT_BASH_PROFILE.value, BashOutputFiles.DOT_BASHRC.value, VimFiles.DOT_VIMRC.value, GitConfigOutputFiles.DOT_GITCONFIG.value ])
  else:
    bashfile.compileBashFiles()
    gitconfig.compileGitConfig()
    createSymlinks()
    cleanUp()
    printCompletionMessage()

if __name__ == '__main__':
  main()
