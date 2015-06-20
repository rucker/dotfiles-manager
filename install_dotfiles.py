#!/usr/bin/python
#  install_dotfiles
#  This script will build platform-specific dotfiles and create the appropriate symlinks in ~

import platform
import os

sysName = platform.system()
os.remove('bashrc')
bashrc = open('bashrc','a')

def writeSection(fileName):
  f = open(fileName,'r')
  for line in f:
    if not line.startswith('#'):
      bashrc.write(line)

writeSection('bash_common')
if os.path.isfile('bash_private'):
  writeSection('bash_private')
if sysName == 'Linux':
  writeSection('bash_linux')
elif sysName == 'Darwin':
  writeSection('bash_mac')
else:
  print "System not supported!"
  bashrc.close()
  exit(1)
bashrc.close()

