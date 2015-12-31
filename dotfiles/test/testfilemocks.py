#!/usr/bin/python

import os
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

from constants import BashInputFiles, BashOutputFiles, VimFiles

def createInputFiles():
  with open(BashInputFiles.BASH_COMMON.value, 'w') as bashCommon:
    bashCommon.write('some_common_token=some_common_value')
  with open(BashInputFiles.BASH_MAC.value, 'w') as bashMac:
    bashMac.write('some_mac_token=some_mac_value')
  with open(BashInputFiles.BASH_LINUX.value, 'w') as bashLinux:
    bashLinux.write('some_linux_token=some_linux_value')
  with open(BashInputFiles.BASH_PRIVATE.value, 'w') as bashPrivate:
    bashPrivate.write('some_private_token=some_private_value')
  with open(VimFiles.VIMRC.value, 'w') as vimrc:
    vimrc.write('someconfigs')

def destroyInputAndOutputFiles():
  for file in [BashInputFiles.BASH_COMMON, BashInputFiles.BASH_MAC, BashInputFiles.BASH_LINUX, BashInputFiles.BASH_PRIVATE, BashOutputFiles.BASH_PROFILE, BashOutputFiles.DOT_BASH_PROFILE, BashOutputFiles.BASHRC, BashOutputFiles.DOT_BASHRC, VimFiles.VIMRC]:
    if os.path.isfile(file.value):
      os.remove(file.value)
  for link in [VimFiles.DOT_VIMRC]:
    if os.path.islink(link.value):
      os.unlink(link.value)
