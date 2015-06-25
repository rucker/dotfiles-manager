#!/usr/bin/python
#  This script will build platform-specific dotfiles and create the appropriate symlinks in ~

import platform
import os
import io
import sys

def init():
  global homeDir
  global destDir

  homeDir = os.path.expanduser('~') + '/'
  destDir = os.path.dirname(os.path.abspath(__file__)) + '/'
  os.chdir(destDir)

def identifySystem():
  global sysName
  global macBashOutputFile
  global macBashOutputDotFile
  global linuxBashOutputFile
  global linuxBashOutputDotFile
  global bashLinux
  global bashMac
  global bashCommon
  global bashPrivate

  sysName = platform.system()
  if sysName != 'Linux' and sysName != 'Darwin':
    print "System not supported!"
    exit(1)
  else:
    print "System identified as " + sysName
    linuxBashOutputFile = 'bashrc'
    linuxBashOutputDotFile = '.' + linuxBashOutputFile
    macBashOutputFile = 'bash_profile'
    macBashOutputDotFile = '.' + macBashOutputFile
    bashLinux = 'bash_linux'
    bashMac = 'bash_mac'
    bashCommon = 'bash_common'
    bashPrivate = 'bash_private'

def cleanUp():
  print "Cleaning up output files in " + destDir + " ..."
  for file in [macBashOutputFile, macBashOutputDotFile, linuxBashOutputFile, linuxBashOutputDotFile]:
    if os.path.isfile(file):
      print "\tRemoving " + file
      os.remove(file)

def handleBashOutputFileWrite(inputFile, contents):
  if hasattr(inputFile, 'name'):
    if inputFile.name == bashLinux:
      outputFiles = [linuxBashOutputFile, linuxBashOutputDotFile]
    elif inputFile.name == bashMac:
      outputFiles = [macBashOutputFile, macBashOutputDotFile]
    elif inputFile.name == bashCommon:
      outputFiles = [linuxBashOutputFile, linuxBashOutputDotFile, macBashOutputFile, macBashOutputDotFile]
    elif inputFile.name == bashPrivate:
      if sysName == 'Linux':
        outputFiles = [linuxBashOutputDotFile]
      elif sysName == 'Darwin':
        outputFiles = [macBashOutputDotFile]
    for file in outputFiles:
      with open(file,'a') as outputFile:
	outputFile.write(contents.getvalue())
  else:
    if inputFile == bashLinux:
      with open(linuxBashOutputDotFile,'a') as bashrc:
	bashrc.write(contents.getvalue())
      with open(linuxBashOutputFile,'a') as bashrc:
	bashrc.write(contents.getvalue())
    else:
      with open(macBashOutputDotFile,'a') as bashrc:
	bashrc.write(contents.getvalue())
      with open(macBashOutputFile,'a') as bashrc:
	bashrc.write(contents.getvalue())

def addBashOutputFileHeader():
  print "Writing " + linuxBashOutputFile + " file header..."
  with io.StringIO() as bashrc:
    bashrc.write(unicode("#!/bin/bash\n"))
    bashrc.write(unicode("# ~/.bashrc: executed by bash(1) for non-login shells.\n"))
    bashrc.write(unicode("# This file was generated by a script. Do not edit manually!\n"))
    handleBashOutputFileWrite(bashLinux, bashrc)
  print "Writing " + macBashOutputFile + " file header..."
  with io.StringIO() as bashrc:
    bashrc.write(unicode("#!/bin/bash\n"))
    bashrc.write(unicode("# ~/.bash_profile: executed by bash(1) for lon-login shells.\n"))
    bashrc.write(unicode("# This file was generated by a script. Do not edit manually!\n"))
    handleBashOutputFileWrite(bashMac, bashrc)

def addInputFileContents(inputFile, allowComments):
  if hasattr(inputFile, 'name'):
    print "\t" + inputFile.name
  with io.StringIO() as bashrc:
    for line in inputFile:
      if line.startswith('#'):
        if allowComments:
          bashrc.write(unicode(line))
      else:
        bashrc.write(unicode(line))
    handleBashOutputFileWrite(inputFile, bashrc)

def createSymlink(targetName, linkName)	:
  target = destDir + targetName
  link = homeDir + linkName
  print "Symlink " + link + " -> " + target
  if os.path.islink(link):
    print "\tLink exists. Checking..."
    try:
      os.stat(link)
    except OSError, e:
      if e.errno == 2:
        print "\tLink is broken. Removing..."
        os.remove(link)
      else:
        raise
    else:
      print "\tLink is valid."
      return
  else:
    print "\tSymlink does not exist. Creating..."
  os.symlink(target, link)
  print "\tLink created."

def install():
  print "Compiling sections..."
  with open('bash_common','r') as bashCommon:
      addInputFileContents(bashCommon,False)
  if os.path.isfile('bash_private'):
    with open('bash_private','r') as bashPrivate:
      addInputFileContents(bashPrivate,False)
  with open('bash_linux','r') as bashLinux:
      addInputFileContents(bashLinux,True)
  with open('bash_mac','r') as bashMac:
      addInputFileContents(bashMac,True)

  createSymlink(macBashOutputDotFile, macBashOutputDotFile)
  createSymlink('vimrc','.vimrc')

  print "Done."

def main():
  init()
  identifySystem()
  cleanUp()
  addBashOutputFileHeader()
  install()

if __name__ == '__main__':
  main()
