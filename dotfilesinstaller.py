#!/usr/bin/python
#  This script will build platform-specific dotfiles and create the appropriate symlinks in ~

import platform
import os
import sys
sysName = ''
homeDir = ''
destDir = ''
def init():
  global homeDir
  global destDir

  homeDir = os.path.expanduser('~') + '/'
  destDir = os.path.dirname(os.path.abspath(__file__)) + '/'
  os.chdir(destDir)

def identifySystem():
  global sysName
  sysName = platform.system()
  if sysName != 'Linux' and sysName != 'Darwin':
    print "System not supported!"
    exit(1)
  else:
    print "System identified as " + sysName

def cleanUp():
  print "Cleaning up files in " + destDir + " ..."
  for file in ['bashrc']:
    if os.path.isfile(file):
      print file
      os.remove(file)

def writeFileHeader():
  global bashrc
  with open('bashrc','a') as bashrc:
    bashrc.write("#!/bin/bash\n")
    if sysName == 'Linux':
      bashrc.write("# ~/.bashrc: executed by bash(1) for non-login shells.\n")
    elif sysName == 'Darwin':
      bashrc.write("# ~/.bash_profile: executed by bash(1) for lon-login shells.\n")
    bashrc.write("# This file was generated by a script. Do not edit manually!\n")

def writeSection(file, allowComments):
  for line in file:
    with open('bashrc','a') as bashrc:
      if line.startswith('#'):
        if allowComments:
          bashrc.write(line)
      else:
        bashrc.write(line)

def createSymlink(targetName, linkName)	:
  target = destDir + targetName
  link = homeDir + linkName
  print "Symlink " + link + " -> " + target
  if os.path.islink(link):
    print "Link exists. Checking..."
    try:
      os.stat(link)
    except OSError, e:
      if e.errno == 2:
        print "Link is broken. Removing..."
        os.remove(link)
      else:
        raise
    else:
      print "Link is valid."
      return
  else:
    print "Symlink does not exist. Creating..."
  os.symlink(target, link)
  print "Link created."

def install():
  with open('bash_common','r') as bashCommon:
      writeSection(bashCommon,False)
  if os.path.isfile('bash_private'):
    with open('bash_private','r') as bashPrivate:
      writeSection(bashPrivate,False)
  if sysName == 'Linux':
    with open('bash_linux','r') as bashLinux:
      writeSection(bashLinux,True)
      createSymlink('bashrc','.bashrc')
  elif sysName == 'Darwin':
    with open('bash_mac','r') as bashMac:
      writeSection(bashMac,True)
      createSymlink('bashrc','.bash_profile')

  createSymlink('vimrc','.vimrc')

if __name__ == '__main__':
  init()
  identifySystem()
  cleanUp()
  writeFileHeader()
  install()
