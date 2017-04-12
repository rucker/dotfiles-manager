from enum import Enum


class SYSTEMS(Enum):
    DARWIN = 'Darwin'
    LINUX = 'Linux'
    WINDOWS = 'Windows'


class DOTFILES(Enum):
    BASH_PROFILE = '.bash_profile'
    BASHRC = '.bashrc'
    GITCONFIG = '.gitconfig'
    VIMRC = '.vimrc'


class SRCFILES(Enum):
    BASH_GLOBAL = 'bash_global'
    BASH_LINUX = 'bash_linux'
    BASH_LOCAL = 'bash_local'
    BASH_MAC_BSD = 'bash_mac_bsd'
    BASH_MAC_GNU = 'bash_mac_gnu'
    GITCONFIG_GLOBAL = 'gitconfig_global'
    GITCONFIG_LOCAL = 'gitconfig_local'
    VIMRC_GLOBAL = 'vimrc_global'
    VIMRC_LOCAL = 'vimrc_local'
