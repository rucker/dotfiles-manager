#!/usr/bin/python

import os
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

from constants import BashInputFiles, BashOutputFiles, VimFiles

def createInputFiles():
  with open(BashInputFiles.BASH_COMMON.value, 'w') as bashCommon:
    bashCommon.write('some_common_token=some_common_value\n')
  with open(BashInputFiles.BASH_MAC.value, 'w') as bashMac:
    bashMac.write('some_mac_token=some_mac_value\n')
  with open(BashInputFiles.BASH_LINUX.value, 'w') as bashLinux:
    bashLinux.write('some_linux_token=some_linux_value\n')
  with open(BashInputFiles.BASH_PRIVATE.value, 'w') as bashPrivate:
    bashPrivate.write('some_private_token=some_private_value\n')
  with open(VimFiles.VIMRC.value, 'w') as vimrc:
    vimrc.write('someconfigs')

def createFile(fileName, contents):
  with open(fileName, 'w') as file:
    file.write('some_token=some_value\n')

def destroyFile(fileName):
  if os.path.isfile(fileName):
    os.remove(fileName)

def destroyInputAndOutputFiles():
  for name, member in BashInputFiles.__members__.items():
    destroyFile(unicode(BashInputFiles[name].value))
  for name, member in BashOutputFiles.__members__.items():
    destroyFile(unicode(BashOutputFiles[name].value))
  destroyFile(VimFiles.VIMRC.value)
  for link in [VimFiles.DOT_VIMRC.value]:
    if os.path.islink(link):
      os.unlink(link)
