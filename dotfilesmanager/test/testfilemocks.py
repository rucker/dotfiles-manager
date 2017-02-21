import os
from os.path import join
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

from dotfilesmanager.test import testenv
from dotfilesmanager.constants import SRCFILES, DOTFILES, SRCFILES
from dotfilesmanager.ioutils import create_file

def createInputFiles():
    create_file(join(testenv.INPUT_DIR, SRCFILES.BASH_GLOBAL.value), 'some_global_token=some_global_value\n')
    create_file(join(testenv.INPUT_DIR, SRCFILES.BASH_MAC_GNU.value), 'some_mac_gnu_token=some_value\n')
    create_file(join(testenv.INPUT_DIR, SRCFILES.BASH_MAC_BSD.value), 'some_mac_bsd_token=some_value\n')
    create_file(join(testenv.INPUT_DIR, SRCFILES.BASH_LINUX.value), 'some_linux_token=some_linux_value\n')
    create_file(join(testenv.INPUT_DIR, SRCFILES.BASH_LOCAL.value), 'some_local_token=some_local_value\n')
    create_file(join(testenv.INPUT_DIR, SRCFILES.GITCONFIG_GLOBAL.value), 'some_gitconfig_token=some_git_config_value')
    create_file(join(testenv.INPUT_DIR, SRCFILES.GITCONFIG_LOCAL.value), 'some_gitconfig_local_token=some_local_git_value')
    create_file(join(testenv.INPUT_DIR, SRCFILES.VIMRC_GLOBAL.value), 'some_vimrc_local_token=some_vimrc_value')
    create_file(join(testenv.INPUT_DIR, SRCFILES.VIMRC_LOCAL.value), 'some_vimrc_local_token=some_local_vimrc_value')
    create_file(testenv.CONFIG_FILE, 'input_dir=some_dir')

