#!/usr/bin/python

import io

import env
from constants import VimrcInputFiles, VimrcOutputFiles
import ioutils

def compileVimrc():
    ioutils.output("Compiling file: " + VimrcOutputFiles.VIMRC.value)
    with io.StringIO() as fileBuffer:
        ioutils.writeRequiredInputFileContents(VimrcInputFiles.VIMRC.value, fileBuffer)
        ioutils.writeOutputFile(env.outputFilesDir + VimrcOutputFiles.VIMRC.value, fileBuffer)
        ioutils.writeOptionalInputFileContents(VimrcInputFiles.VIMRC_LOCAL.value, fileBuffer)
        ioutils.writeOutputFile(env.homeDir + VimrcOutputFiles.DOT_VIMRC.value, fileBuffer)
        ioutils.output("File completed.\n")
