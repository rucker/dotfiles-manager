#!/usr/bin/python

from enum import Enum

class Systems(Enum):
    DARWIN = 'Darwin'
    LINUX = 'Linux'
    WINDOWS = 'Windows'

class BashInputFiles(Enum):
    BASH_COMMON = 'bash_common'
    BASH_MAC_BSD = 'bash_mac_bsd'
    BASH_MAC_GNU = 'bash_mac_gnu'
    BASH_LINUX = 'bash_linux'
    BASH_LOCAL = 'bash_local'

class BashOutputFiles(Enum):
    BASH_PROFILE = 'bash_profile'
    DOT_BASH_PROFILE = '.bash_profile'
    BASHRC = 'bashrc'
    DOT_BASHRC = '.bashrc'
    BASH_ALIASES = 'bash_aliases'

class VimFiles(Enum):
    VIMRC = 'vimrc'
    DOT_VIMRC = '.vimrc'

class GitConfigInputFiles(Enum):
    GITCONFIG = 'gitconfig'
    GITCONFIG_LOCAL = 'gitconfig_local'

class GitConfigOutputFiles(Enum):
    GITCONFIG = 'gitconfig'
    DOT_GITCONFIG = '.gitconfig'
