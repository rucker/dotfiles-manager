#!/usr/bin/python

import os
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
from constants import Srcfiles, Dotfiles, Srcfiles

def createInputFiles():
    with open(env.srcDir + Srcfiles.BASH_COMMON.value, 'w') as bashCommon:
        bashCommon.write('some_common_token=some_common_value\n')
    with open(env.srcDir + Srcfiles.BASH_MAC_GNU.value, 'w') as bashMac:
        bashMac.write('some_mac_token=some_mac_value\n')
    with open(env.srcDir + Srcfiles.BASH_LINUX.value, 'w') as bashLinux:
        bashLinux.write('some_linux_token=some_linux_value\n')
    with open(env.srcDir + Srcfiles.BASH_LOCAL.value, 'w') as bashLocal:
        bashLocal.write('some_local_token=some_local_value\n')
    with open(env.outputDir + Dotfiles.VIMRC.value, 'w') as vimrc:
        vimrc.write('someconfigs')
    with open(env.srcDir + Srcfiles.GITCONFIG.value, 'w') as gitConfig:
        gitConfig.write('some_gitconfig_token=some_git_config_value')
    with open(env.srcDir + Srcfiles.GITCONFIG_LOCAL.value, 'w') as gitLocal:
        gitLocal.write('some_gitconfig_local_token=some_local_git_value')
    with open(env.srcDir + Srcfiles.VIMRC.value, 'w') as vimrcLocal:
        vimrcLocal.write('some_vimrc_local_token=some_vimrc_value')
    with open(env.srcDir + Srcfiles.VIMRC_LOCAL.value, 'w') as vimrcLocal:
        vimrcLocal.write('some_vimrc_local_token=some_local_vimrc_value')

def createFile(fileName, contents):
    with open(fileName, 'w') as file:
        file.write('some_token=some_value\n')

def destroyFile(fileName):
    if os.path.isfile(fileName):
        os.remove(fileName)
