#!/usr/bin/python

import io
import os
import time
import glob

import env

def backupFile(fileName):
  timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
  backupFile = env.backupsDir + fileName[fileName.rfind('/') + 1 :].replace('.','') + '_' + timestamp + '.bak'
  print "\tBacking up " + fileName + " to " + backupFile
  os.rename(fileName, backupFile)

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
  if not env.args.clobber and os.path.isfile(filePath) and env.outputFilesDir not in filePath:
    backupFile(filePath)
  print "\tWriting output file " + filePath
  with open(filePath, 'w') as outputFile:
    outputFile.write(fileBuffer.getvalue())

def revertDotFiles(fileNames):
  for file in fileNames:
    name = file.replace('.','')
    searchPattern = env.backupsDir + '*' + name + '*'
    print 'search pattern: ' + searchPattern
    results = sorted(glob.glob(searchPattern), reverse=True)
    if results:
      bakFile = results[0]
      print bakFile
      choice = ''
      while choice not in (['Y','N']):
        choice = raw_input("Revert " + file + " to backup located at " + bakFile + "? (Y/N): ").upper()
        if choice == 'Y':
          os.remove(env.homeDir + file)
          os.rename(bakFile, env.homeDir + file)
