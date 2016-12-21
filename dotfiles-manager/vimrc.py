#!/usr/bin/python

import io

import env
from constants import Srcfiles, Dotfiles
import ioutils

def compileVimrc():
    ioutils.output("Compiling file: " + Dotfiles.VIMRC.value)
    with io.StringIO() as fileBuffer:
        ioutils.writeRequiredInputFileContents(Srcfiles.VIMRC.value, fileBuffer)
        if env.args.no_local == False:
            ioutils.writeOptionalInputFileContents(Srcfiles.VIMRC_LOCAL.value, fileBuffer)
        ioutils.writeOutputFile(env.outputDir + Dotfiles.VIMRC.value, fileBuffer)
        ioutils.output("File completed.\n")
