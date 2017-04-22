from os.path import join
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

from dotfilesmanager.test import testenv
from dotfilesmanager.constants import BASHFILES
from dotfilesmanager.ioutils import create_file

def createInputFiles():
    gitconfig = 'gitconfig'
    gitconfig_local = 'gitconfig_local'

    vimrc= 'vimrc'
    vimrc_local = 'vimrc_local'

    create_file(join(testenv.INPUT_DIR, BASHFILES.BASH_GLOBAL.value), 'some_global_token=some_global_value\n')
    create_file(join(testenv.INPUT_DIR, BASHFILES.BASH_MAC_GNU.value), 'some_mac_gnu_token=some_value\n')
    create_file(join(testenv.INPUT_DIR, BASHFILES.BASH_MAC_BSD.value), 'some_mac_bsd_token=some_value\n')
    create_file(join(testenv.INPUT_DIR, BASHFILES.BASH_LINUX.value), 'some_linux_token=some_linux_value\n')
    create_file(join(testenv.INPUT_DIR, BASHFILES.BASH_LOCAL.value), 'some_local_token=some_local_value\n')
    create_file(join(testenv.INPUT_DIR, gitconfig), 'some_gitconfig_token=some_git_config_value')
    create_file(join(testenv.INPUT_DIR, gitconfig_local), 'some_gitconfig_local_token=some_local_git_value')
    create_file(join(testenv.INPUT_DIR, vimrc), 'some_vimrc_local_token=some_vimrc_value')
    create_file(join(testenv.INPUT_DIR, vimrc_local), 'some_vimrc_local_token=some_local_vimrc_value')
