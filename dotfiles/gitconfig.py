#!/usr/bin/python

import io

import env
from constants import GitConfigInputFiles, GitConfigOutputFiles
import filewriter

def compileGitConfig():
  print "Compiling file: " + GitConfigOutputFiles.GITCONFIG.value
  with io.StringIO() as fileBuffer:
    filewriter.writeInputFileContents(GitConfigInputFiles.GIT_PUBLIC.value, fileBuffer)
    filewriter.writeOutputFile(env.outputFilesDir + GitConfigOutputFiles.GITCONFIG.value, fileBuffer)
    filewriter.writeOptionalInputFileContents(GitConfigInputFiles.GIT_PRIVATE.value, fileBuffer)
    filewriter.writeOutputFile(env.homeDir + GitConfigOutputFiles.DOT_GITCONFIG.value, fileBuffer)
    print "File completed.\n"
