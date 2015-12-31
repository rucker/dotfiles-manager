#!/usr/bin/python

import os
from constants import BashInputFiles, BashOutputFiles

def createInputFiles():
  with open(BashInputFiles.BASH_COMMON.value, 'w') as bashCommon:
    bashCommon.write('some_common_token=some_common_value')
  with open(BashInputFiles.BASH_MAC.value, 'w') as bashMac:
    bashMac.write('some_mac_token=some_mac_value')
  with open(BashInputFiles.BASH_LINUX.value, 'w') as bashLinux:
    bashLinux.write('some_linux_token=some_linux_value')
  with open(BashInputFiles.BASH_PRIVATE.value, 'w') as bashPrivate:
    bashPrivate.write('some_private_token=some_private_value')

def destroyInputAndOutputFiles():
  for file in [BashInputFiles.BASH_COMMON.value, BashInputFiles.BASH_MAC.value, BashInputFiles.BASH_LINUX.value, BashInputFiles.BASH_PRIVATE.value, BashOutputFiles.BASH_PROFILE.value, BashOutputFiles.DOT_BASH_PROFILE.value, BashOutputFiles.BASHRC.value, BashOutputFiles.DOT_BASHRC.value]:
    if os.path.isfile(file):
      os.remove(file)
