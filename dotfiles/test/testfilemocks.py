#!/usr/bin/python

import os
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
from constants import BashInputFiles, VimFiles, GitConfigInputFiles

def createInputFiles():
  with open(env.inputFilesDir + BashInputFiles.BASH_COMMON.value, 'w') as bashCommon:
    bashCommon.write('some_common_token=some_common_value\n')
  with open(env.inputFilesDir + BashInputFiles.BASH_MAC.value, 'w') as bashMac:
    bashMac.write('some_mac_token=some_mac_value\n')
  with open(env.inputFilesDir + BashInputFiles.BASH_LINUX.value, 'w') as bashLinux:
    bashLinux.write('some_linux_token=some_linux_value\n')
  with open(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value, 'w') as bashPrivate:
    bashPrivate.write('some_private_token=some_private_value\n')
  with open(env.outputFilesDir + VimFiles.VIMRC.value, 'w') as vimrc:
    vimrc.write('someconfigs')
  with open(env.inputFilesDir + GitConfigInputFiles.GIT_PUBLIC.value, 'w') as gitPublic:
    gitPublic.write('some_git_public_token=some_public_git_value')
  with open(env.inputFilesDir + GitConfigInputFiles.GIT_PRIVATE.value, 'w') as gitPrivate:
    gitPrivate.write('some_git_private_token=some_private_git_value')

def createFile(fileName, contents):
  with open(fileName, 'w') as file:
    file.write('some_token=some_value\n')

def destroyFile(fileName):
  if os.path.isfile(fileName):
    os.remove(fileName)
