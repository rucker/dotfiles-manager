#!/usr/bin/python

import io
import os
import time
import glob
import shutil

import env
from constants import Srcfiles, Dotfiles
import ioutils

def backupFile(fileName):
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    backupFile = env.backupsDir + fileName[fileName.rfind('/') + 1 :].replace('.','') + '_' + timestamp + '.bak'
    output("\tBacking up " + fileName + " to " + backupFile)
    shutil.move(fileName, backupFile)

def writeToOutputBuffer(output, fileBuffer):
    fileBuffer.write(unicode(output))

def writeOptionalInputFileContents(fileName, fileBuffer):
    if os.path.isfile(env.inputDir + fileName):
        writeInputFileContents(fileName, fileBuffer)
    else:
        output("\t" + fileName + " is not present. Skipping...")

def writeRequiredInputFileContents(fileName, fileBuffer):
    if os.path.isfile(env.inputDir + fileName):
        writeInputFileContents(fileName, fileBuffer)
    else:
        msg = "Required input file " + fileName + " is not present. Please replace the file and try again."
        if (env.args.verbose):
                msg = "\t" + msg
        print msg
        exit(1)

def writeInputFileContents(fileName, fileBuffer):
    with open(env.inputDir + fileName) as inputFile:
        output("\tReading input file " + fileName)
        for line in inputFile:
            writeToOutputBuffer(line, fileBuffer)

def writeOutputFile(filePath, fileBuffer):
    if not env.args.clobber and os.path.isfile(filePath) and env.outputDir not in filePath:
        backupFile(filePath)
    output("\tWriting output file " + filePath)
    with open(filePath, 'w') as outputFile:
        outputFile.write(fileBuffer.getvalue())

def revertDotfiles(fileNames):
    for file in fileNames:
        name = file.replace('.','')
        searchPattern = env.backupsDir + '*' + name + '*'
        output("search pattern: " + searchPattern)
        results = sorted(glob.glob(searchPattern), reverse=True)
        if results:
            bakFile = results[0]
            print bakFile
            choice = ''
            while choice not in (['Y','N']):
                choice = raw_input("Revert " + file + " to backup located at " + bakFile + "? (Y/N): ").upper()
                if choice == 'Y':
                    os.remove(env.outputDir + file)
                    shutil.move(bakFile, env.outputDir + file)

def output(str):
    if (env.args.verbose):
        print str

def compileDotfile(fileName):
    ioutils.output("Compiling file: " + fileName)
    with io.StringIO() as fileBuffer:
        #TODO better way to get output file name?
        inputFileName = fileName[fileName.rfind('/') + 1 :].replace('.','')
        ioutils.writeRequiredInputFileContents(inputFileName, fileBuffer)
        if env.args.no_local == False:
            #TODO better way to get local file name?
            ioutils.writeOptionalInputFileContents(inputFileName + "_local", fileBuffer)
        ioutils.writeOutputFile(env.outputDir + fileName, fileBuffer)
        ioutils.output("File completed.\n")
