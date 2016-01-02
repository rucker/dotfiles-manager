#!/usr/bin/python

import io
import os

import env
from constants import Systems, BashInputFiles, BashOutputFiles

def writeHeader(fileName, fileBuffer):
  fileBuffer.write(unicode("#!/bin/bash\n# ~/" + fileName + ": executed by bash(1) for non-login shells.\n# This file was generated by a script. Do not edit manually!\n"))

def writeInputFileContents(fileName, fileBuffer):
  with open(env.inputFilesDir + fileName) as inputFile:
    print "\tSourcing input file " + fileName
    for line in inputFile:
      fileBuffer.write(unicode(line))

def writeOutputFile(filePath, fileBuffer):
  print "\tWriting output file " + filePath
  with open(filePath, 'w') as outputFile:
    outputFile.write(fileBuffer.getvalue())

def compileBashFile(platform):
  if platform is Systems.DARWIN.value:
    bashFile = BashOutputFiles.BASH_PROFILE.value
    bashDotFile = BashOutputFiles.DOT_BASH_PROFILE.value
    bashPlatformFile = BashInputFiles.BASH_MAC.value
  elif platform is Systems.LINUX.value:
    bashFile = BashOutputFiles.BASHRC.value
    bashDotFile = BashOutputFiles.DOT_BASHRC.value
    bashPlatformFile = BashInputFiles.BASH_LINUX.value
  print "Compiling file: " + bashFile
  with io.StringIO() as fileBuffer:
    writeHeader(bashDotFile, fileBuffer)
    writeInputFileContents(BashInputFiles.BASH_COMMON.value, fileBuffer)
    writeInputFileContents(bashPlatformFile, fileBuffer)
    writeOutputFile(env.outputFilesDir + bashFile, fileBuffer)
    if env.platform is platform:
      if os.path.isfile(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value):
	writeInputFileContents(BashInputFiles.BASH_PRIVATE.value, fileBuffer)
	writeOutputFile(env.homeDir + bashDotFile, fileBuffer)
      else:
	print BashInputFiles.BASH_PRIVATE.value + " is not present. Skipping..."
    print "File completed."

def compileBashProfile():
  compileBashFile(Systems.DARWIN.value)
def compileBashrc():
  compileBashFile(Systems.LINUX.value)

def compileBashFiles():
  compileBashProfile()
  compileBashrc()
