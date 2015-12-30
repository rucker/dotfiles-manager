#!/usr/bin/python

from enum import Enum

class Systems(Enum):
  DARWIN = 'Darwin'
  LINUX = 'Linux'
  WINDOWS = 'Windows'

class BashInputFiles(Enum):
  BASH_COMMON = 'bash_common'
  BASH_MAC = 'bash_mac'
  BASH_LINUX = 'bash_linux'
  BASH_PRIVATE = 'bash_private'
