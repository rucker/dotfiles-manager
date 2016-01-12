#!/usr/bin/python

import io
import env

def writeToOutputBuffer(output, fileBuffer):
  fileBuffer.write(unicode(output))

def writeInputFileContents(fileName, fileBuffer):
  with open(env.inputFilesDir + fileName) as inputFile:
    print "\tReading input file " + fileName
    for line in inputFile:
      fileBuffer.write(unicode(line))

def writeOutputFile(filePath, fileBuffer):
  print "\tWriting output file " + filePath
  with open(filePath, 'w') as outputFile:
    outputFile.write(fileBuffer.getvalue())

