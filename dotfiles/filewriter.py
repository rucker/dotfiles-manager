#!/usr/bin/python

import io
import os

import env

def backupFile(fileName):
  print "\tThe file " + fileName + " already exists. Renaming to " + fileName + ".bak"
  os.rename(fileName, fileName + ".bak")

def writeToOutputBuffer(output, fileBuffer):
  fileBuffer.write(unicode(output))

def writeOptionalInputFileContents(fileName, fileBuffer):
  if os.path.isfile(env.inputFilesDir + fileName):
    writeInputFileContents(fileName, fileBuffer)
  else:
    print "\t" + fileName + " is not present. Skipping..."

def writeInputFileContents(fileName, fileBuffer):
  with open(env.inputFilesDir + fileName) as inputFile:
    print "\tReading input file " + fileName
    for line in inputFile:
      writeToOutputBuffer(line, fileBuffer)

def writeOutputFile(filePath, fileBuffer):
  if os.path.isfile(filePath):
    backupFile(filePath)
  print "\tWriting output file " + filePath
  with open(filePath, 'w') as outputFile:
    outputFile.write(fileBuffer.getvalue())

