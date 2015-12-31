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

class BashOutputFiles(Enum):
  BASH_PROFILE = 'bash_profile'
  DOT_BASH_PROFILE = '.bash_profile'
  BASHRC = 'bashrc'
  DOT_BASHRC = '.bashrc'

class VimFiles(Enum):
  VIMRC = 'vimrc'
  DOT_VIMRC = '.vimrc'