#!/usr/bin/python

import sys
import platform
import io
import os
import argparse

from constants import Systems, BashOutputFiles, VimFiles, GitConfigOutputFiles
import bashfile
import gitconfig
import env
import ioutils

def init():
    identifySystem()
    setArgs()
    setEnv()
    os.chdir(env.workingDir)

def identifySystem():
    supportedPlatforms = [Systems.DARWIN.value, Systems.LINUX.value]
    env.platform = platform.system()
    if env.platform not in supportedPlatforms:
        ioutils.output("System not supported!")
        exit(1)

    if env.platform == Systems.LINUX.value or os.path.isdir('/usr/local/opt/coreutils/libexec/gnubin/'):
        env.isGnu = True
    else:
        env.isGnu = False

def setArgs():
    env.parser = argparse.ArgumentParser(description="Compile your custom dotfiles from input files.")
    env.parser.add_argument('-c', '--clobber', action='store_true', help="Clobber any existing output files (don't back them up).")
    env.parser.add_argument('-r', '--revert', action='store_true', help="Revert dotfiles to most recent backup.")
    env.parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    env.args = env.parser.parse_args()
    ioutils.output("\nPreparing dotfiles!\n")

def setEnv():
    env.homeDir = os.path.expanduser('~') + '/'
    env.workingDir = os.path.dirname(os.path.realpath(__file__)) + '/'
    env.inputFilesDir = env.workingDir + 'inputfiles/'
    env.scriptsDir = env.workingDir + 'scripts/'
    env.outputFilesDir = env.workingDir[:env.workingDir.rfind('dotfiles/')]
    env.backupsDir = env.workingDir + 'backups/'

    ioutils.output("Environment:")
    ioutils.output("\tplatform: " + env.platform)
    ioutils.output("\thomeDir: " + env.homeDir)
    ioutils.output("\tworkingDir: " + env.workingDir)
    ioutils.output("\tinputFilesDir: " + env.inputFilesDir)
    ioutils.output("\tscriptsDir: " + env.scriptsDir)
    ioutils.output("\toutputFilesDir: " + env.outputFilesDir)
    ioutils.output("\tbackupsDir: " + env.backupsDir)
    ioutils.output("\targs: " + str(env.args))
    ioutils.output("")

def symlink(target, linkName) :
    ioutils.output("Symlink " + linkName + " -> " + target)
    if os.path.islink(linkName):
        ioutils.output("\tLink already exists.\n")
        return
    elif os.path.isfile(linkName):
        ioutils.backupFile(linkName)
    else:
        ioutils.output("\tSymlink does not exist.")
    ioutils.output("\tCreating...")
    os.symlink(target, linkName)
    ioutils.output("\tLink created.\n")

def createSymlinks():
    symlink(env.outputFilesDir + VimFiles.VIMRC.value, env.homeDir + VimFiles.DOT_VIMRC.value)

def printCompletionMessage():
    if env.platform == Systems.DARWIN.value:
        bashFileName = BashOutputFiles.DOT_BASH_PROFILE.value
    else:
        bashFileName = BashOutputFiles.DOT_BASHRC.value
    print "Done. Recommend you source ~/" + bashFileName + " or start new a terminal session."

def main():
    init()
    if env.args.revert:
        ioutils.revertDotFiles([ BashOutputFiles.DOT_BASH_PROFILE.value, BashOutputFiles.DOT_BASHRC.value, VimFiles.DOT_VIMRC.value, GitConfigOutputFiles.DOT_GITCONFIG.value ])
    else:
        bashfile.compileBashFiles()
        gitconfig.compileGitConfig()
        createSymlinks()
        printCompletionMessage()

if __name__ == '__main__':
    main()
