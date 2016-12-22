#!/usr/bin/python

import sys
import platform
import io
import os
import argparse

from constants import Systems, Dotfiles, Srcfiles
import bashfile
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
    env.parser.add_argument('-n', '--no-local', action='store_true', help="Skip _local input files during compilation.")
    env.parser.add_argument('-o', '--output-dir', nargs='?', default=os.environ['HOME'], help="Specify output directory.")
    env.args = env.parser.parse_args()
    ioutils.output("\nPreparing dotfiles!\n")

def setEnv():
    env.workingDir = os.path.dirname(os.path.realpath(__file__)) + '/'
    env.srcDir = env.workingDir + 'src/'
    env.scriptsDir = env.workingDir + 'scripts/'
    env.outputDir = env.args.output_dir
    env.backupsDir = env.workingDir + 'backups/'

    ioutils.output("Environment:")
    ioutils.output("\tplatform: " + env.platform)
    ioutils.output("\tworkingDir: " + env.workingDir)
    ioutils.output("\tsrcDir: " + env.srcDir)
    ioutils.output("\tscriptsDir: " + env.scriptsDir)
    ioutils.output("\toutputDir: " + env.outputDir)
    ioutils.output("\tbackupsDir: " + env.backupsDir)
    ioutils.output("\targs: " + str(env.args))
    ioutils.output("")

def printCompletionMessage():
    if env.platform == Systems.DARWIN.value:
        bashFileName = Dotfiles.BASH_PROFILE.value
    else:
        bashFileName = Dotfiles.BASHRC.value
    print "Done. Recommend you source ~/" + bashFileName + " or start new a terminal session."

def main():
    init()
    if env.args.revert:
        ioutils.revertDotfiles([ Dotfiles.BASH_PROFILE.value, Dotfiles.BASHRC.value, Dotfiles.VIMRC.value, Dotfiles.GITCONFIG.value ])
    else:
        bashfile.compileBashFiles()
        ioutils.compileDotfile(Srcfiles.VIMRC.value)
        ioutils.compileDotfile(Srcfiles.GITCONFIG.value)
        printCompletionMessage()

if __name__ == '__main__':
    main()
