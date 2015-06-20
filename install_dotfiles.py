#!/usr/bin/python
#  install_dotfiles
#  This script will build platform-specific dotfiles and create the appropriate symlinks in ~

import platform
import os

sysName = platform.system()
os.remove('bashrc')
bashrc = open('bashrc','a')

def writeSection(fileName, allowComments):
  f = open(fileName,'r')
  for line in f:
    if line.startswith('#'):
      if allowComments:
        bashrc.write(line)
    else:
      bashrc.write(line)

if sysName == 'Linux':
  writeSection('bash_linux',True)
elif sysName == 'Darwin':
  writeSection('bash_mac',True)
else:
  print "System not supported!"
  bashrc.close()
  exit(1)
if os.path.isfile('bash_private'):
  writeSection('bash_private',False)
writeSection('bash_common',False)
bashrc.close()

