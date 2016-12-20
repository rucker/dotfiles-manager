#!/usr/bin/python

import io

import env
from constants import GitConfigInputFiles, GitConfigOutputFiles
import ioutils

def compileGitConfig():
    ioutils.output("Compiling file: " + GitConfigOutputFiles.GITCONFIG.value)
    with io.StringIO() as fileBuffer:
        ioutils.writeRequiredInputFileContents(GitConfigInputFiles.GITCONFIG.value, fileBuffer)
        ioutils.writeOutputFile(env.outputFilesDir + GitConfigOutputFiles.GITCONFIG.value, fileBuffer)
        ioutils.writeOptionalInputFileContents(GitConfigInputFiles.GITCONFIG_LOCAL.value, fileBuffer)
        ioutils.writeOutputFile(env.homeDir + GitConfigOutputFiles.DOT_GITCONFIG.value, fileBuffer)
        ioutils.output("File completed.\n")
