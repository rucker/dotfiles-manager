#!/usr/bin/python

import io
import os

import env

def cleanUpRenamedFiles(fileNames):
  for fileName in fileNames:
    newFile = env.homeDir + fileName
    bakFile = newFile + '.bak'
    if os.path.isfile(bakFile):
      choice = ''
      print "The existing file " + newFile + " was renamed to " + bakFile + "."
      while choice not in ['Y','N']:
	choice = raw_input("Would you like to delete it? (Y/N): ").upper()
	if choice == 'Y':
	  os.remove(bakFile)
	  print "Deleting file " + bakFile + "."
	elif choice == 'N':
	  print "Keeping file " + bakFile + "."

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
  if '-c' not in env.args and os.path.isfile(filePath) and env.outputFilesDir not in filePath:
    backupFile(filePath)
  print "\tWriting output file " + filePath
  with open(filePath, 'w') as outputFile:
    outputFile.write(fileBuffer.getvalue())

