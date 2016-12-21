#!/usr/bin/python

import io

import env
from constants import Srcfiles, Dotfiles
import ioutils

def compileGitConfig():
    ioutils.output("Compiling file: " + Dotfiles.GITCONFIG.value)
    with io.StringIO() as fileBuffer:
        ioutils.writeRequiredInputFileContents(Srcfiles.GITCONFIG.value, fileBuffer)
        if env.args.no_local == False:
            ioutils.writeOptionalInputFileContents(Srcfiles.GITCONFIG_LOCAL.value, fileBuffer)
        ioutils.writeOutputFile(env.outputDir + Dotfiles.GITCONFIG.value, fileBuffer)
        ioutils.output("File completed.\n")
