#!/usr/bin/python

from enum import Enum

class Systems(Enum):
    DARWIN = 'Darwin'
    LINUX = 'Linux'
    WINDOWS = 'Windows'

class Dotfiles(Enum):
    BASH_PROFILE = '.bash_profile'
    BASHRC = '.bashrc'
    GITCONFIG = '.gitconfig'
    VIMRC = '.vimrc'

class Srcfiles(Enum):
    BASH_COMMON = 'bash_common'
    BASH_LINUX = 'bash_linux'
    BASH_LOCAL = 'bash_local'
    BASH_MAC_BSD = 'bash_mac_bsd'
    BASH_MAC_GNU = 'bash_mac_gnu'
    GITCONFIG = 'gitconfig'
    GITCONFIG_LOCAL = 'gitconfig_local'
    VIMRC = 'vimrc'
    VIMRC_LOCAL = 'vimrc_local'

class Misc(Enum):
    CONFIG_FILE = '.dotfilesrc'
