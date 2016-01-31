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

def mapInputFileContents(fileName, dict):
  with open (env.inputFilesDir + fileName) as inputFile:
    for line in inputFile:
      pair = line.split('=')
      if len(pair) == 2:
	dict[pair[0]] = pair[1]

def mapOptionalInputFileContents(fileName, dict):
  if os.path.isfile(env.inputFilesDir + fileName):
    mapInputFileContents(fileName, dict)
  else:
    print "\t" + fileName + " is not present. Skipping..."

def handleExistingFile(filePath):
  if not env.args.clobber and os.path.isfile(filePath) and env.outputFilesDir not in filePath:
    backupFile(filePath)

def dictToBuffer(dict):
  buffer = io.StringIO()
  for k,v in dict.items():
    buffer.write(unicode(k + '=' + v))
  return buffer

def writeOutputFile(filePath, *buffer):
  with open(filePath, 'w') as outputFile:
    for b in buffer:
      outputFile.write(b.getvalue())

