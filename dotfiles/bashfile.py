#!/usr/bin/python

import io
import os

import env
import ioutils
from constants import Systems, BashInputFiles, BashOutputFiles

def appendEnvScriptsDirToOutputBuffer(fileBuffer):
  ioutils.writeToOutputBuffer("scriptsDir=\"" + env.scriptsDir + "\"\n\n", fileBuffer)

def writeHeader(fileName, fileBuffer):
  ioutils.writeToOutputBuffer("#!/bin/bash\n# ~/" + fileName + ": executed by bash(1) for non-login shells.\n# This file was generated by a script. Do not edit manually!\n\n", fileBuffer)

def compileBashFile(platform):
  if platform == Systems.DARWIN.value:
    bashFile = BashOutputFiles.BASH_PROFILE.value
    bashDotFile = BashOutputFiles.DOT_BASH_PROFILE.value
    if env.isGnu == True:
      bashPlatformFile = BashInputFiles.BASH_MAC_GNU.value
    else:
      bashPlatformFile = BashInputFiles.BASH_MAC_BSD.value
  elif platform == Systems.LINUX.value:
    bashFile = BashOutputFiles.BASHRC.value
    bashDotFile = BashOutputFiles.DOT_BASHRC.value
    bashPlatformFile = BashInputFiles.BASH_LINUX.value

  ioutils.output("Compiling file: " + bashFile)
  with io.StringIO() as fileBuffer:
    writeHeader(bashDotFile, fileBuffer)
    appendEnvScriptsDirToOutputBuffer(fileBuffer)
    ioutils.writeRequiredInputFileContents(BashInputFiles.BASH_COMMON.value, fileBuffer)
    ioutils.writeOptionalInputFileContents(bashPlatformFile, fileBuffer)
    ioutils.writeOutputFile(env.outputFilesDir + bashFile, fileBuffer)
    if env.platform == platform:
      ioutils.writeOptionalInputFileContents(BashInputFiles.BASH_PRIVATE.value, fileBuffer)
      ioutils.writeOutputFile(env.homeDir + bashDotFile, fileBuffer)
    ioutils.output("File completed.\n")

def compileBashProfile():
  compileBashFile(Systems.DARWIN.value)
def compileBashrc():
  compileBashFile(Systems.LINUX.value)

def compileBashFiles():
  compileBashProfile()
  compileBashrc()
