#!/usr/bin/python

import io

import env
from constants import GitConfigInputFiles, GitConfigOutputFiles
import ioutils

def compileGitConfig():
  ioutils.output("Compiling file: " + GitConfigOutputFiles.GITCONFIG.value)
  with io.StringIO() as fileBuffer:
    ioutils.writeInputFileContents(GitConfigInputFiles.GIT_PUBLIC.value, fileBuffer)
    ioutils.writeOutputFile(env.outputFilesDir + GitConfigOutputFiles.GITCONFIG.value, fileBuffer)
    ioutils.writeOptionalInputFileContents(GitConfigInputFiles.GIT_PRIVATE.value, fileBuffer)
    ioutils.writeOutputFile(env.homeDir + GitConfigOutputFiles.DOT_GITCONFIG.value, fileBuffer)
    ioutils.output("File completed.\n")
