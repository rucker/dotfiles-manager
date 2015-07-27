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
  global inputFilesDir
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
    inputFilesDir = '../inputfiles/'
    print "System identified as " + sysName
    linuxBashOutputFile = 'bashrc'
    linuxBashOutputDotFile = '.' + linuxBashOutputFile
    macBashOutputFile = 'bash_profile'
    macBashOutputDotFile = '.' + macBashOutputFile
    bashLinux = inputFilesDir + 'bash_linux'
    bashMac = inputFilesDir + 'bash_mac'
    bashCommon = inputFilesDir + 'bash_common'
    bashPrivate = inputFilesDir + 'bash_private'

def cleanUp():
  print "Cleaning up output files in " + destDir + " ..."
  for file in [macBashOutputFile, macBashOutputDotFile, linuxBashOutputFile, linuxBashOutputDotFile]:
    if os.path.isfile(file):
      print "\tRemoving " + file
      os.remove(file)

def handleBashOutputFileWrite(inputFile, contents):
  if hasattr(inputFile, 'name'): #It's an input file
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
  else: #It's the file header StringIO
    if inputFile == linuxBashOutputDotFile:
      outputFiles = [linuxBashOutputFile, linuxBashOutputDotFile]
    elif inputFile == macBashOutputDotFile:
      outputFiles = [macBashOutputFile, macBashOutputDotFile]
  for file in outputFiles:
    with open(file,'a') as outputFile:
      outputFile.write(contents.getvalue())

def addBashOutputFileHeader():
  headerText = "#!/bin/bash\n# ~/{fileName}: executed by bash(1) for non-login shells.\n# This file was generated by a script. Do not edit manually!\n"
  for file in [linuxBashOutputDotFile, macBashOutputDotFile]:
    print "Writing " + file + " file header..."
    with io.StringIO() as bashrc:
      bashrc.write(unicode(headerText.replace("{fileName}", file)))
      handleBashOutputFileWrite(file, bashrc)

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
  elif os.path.isfile(link):
    print "\tLink source is regular file. Renaming to " + homeDir + linkName + '.bak'
    os.rename(link, homeDir + linkName + '.bak')
  else:
    print "\tSymlink does not exist. Creating..."
  os.symlink(target, link)
  print "\tLink created."

def install():
  print "Compiling sections..."
  with open(inputFilesDir + 'bash_common','r') as bashCommon:
      addInputFileContents(bashCommon,False)
  if os.path.isfile(inputFilesDir + 'bash_private'):
    with open(inputFilesDir + 'bash_private','r') as bashPrivate:
      addInputFileContents(bashPrivate,False)
  with open(inputFilesDir + 'bash_linux','r') as bashLinux:
      addInputFileContents(bashLinux,True)
  with open(inputFilesDir + 'bash_mac','r') as bashMac:
      addInputFileContents(bashMac,True)

  if sysName == 'Linux':
    createSymlink(linuxBashOutputDotFile, linuxBashOutputDotFile)
  else:
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
