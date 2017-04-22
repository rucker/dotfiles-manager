from enum import Enum


class SYSTEMS(Enum):
    DARWIN = 'Darwin'
    LINUX = 'Linux'
    WINDOWS = 'Windows'


class BASHFILES(Enum):
    BASH_PROFILE = '.bash_profile'
    BASHRC = '.bashrc'
    BASH_GLOBAL = 'bash'
    BASH_LINUX = 'bash_linux'
    BASH_LOCAL = 'bash_local'
    BASH_MAC_BSD = 'bash_mac_bsd'
    BASH_MAC_GNU = 'bash_mac_gnu'
