#!/usr/bin/python

import sys
import os
import unittest

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import dotfiles
import testfilemocks
import bashfile
from constants import Systems, BashInputFiles, BashOutputFiles

class BashFileIntTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    dotfiles.init()
    env.inputFilesDir = ''
    env.outputFilesDir = ''
    env.homeDir = ''
    testfilemocks.createInputFiles()

  @classmethod
  def tearDownClass(self):
    testfilemocks.destroyInputAndOutputFiles()

  def testBashCommonAndBashMacWrittenToBashProfile(self):
    env.platform = Systems.DARWIN.value
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value) as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_COMMON.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)
      with open(env.inputFilesDir + BashInputFiles.BASH_MAC.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)

  def testBashLinuxNotWrittenToBashProfile(self):
    env.platform = Systems.DARWIN.value
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value) as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_LINUX.value) as bashInput:
        self.assertTrue(bashInput.read() not in contents)

  def testBashPrivateNotWrittenToBashProfileInWorkingDir(self):
    env.platform = Systems.DARWIN.value
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value) as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value) as bashInput:
        self.assertTrue(bashInput.read() not in contents)

  def testBashPrivateWrittenToBashProfileInHomeDir(self):
    env.platform = Systems.DARWIN.value
    bashfile.compileBashProfile()
    with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value) as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)

  def testBashCommonAndBashLinuxWrittenToBashrc(self):
    env.platform = Systems.LINUX.value
    bashfile.compileBashrc()
    with open(env.outputFilesDir + BashOutputFiles.BASHRC.value) as bashrc:
      contents = bashrc.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_COMMON.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)
      with open(env.inputFilesDir + BashInputFiles.BASH_LINUX.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)

  def testBashMacNotWrittenToBashrc(self):
    env.platform = Systems.LINUX.value
    bashfile.compileBashrc()
    with open(env.outputFilesDir + BashOutputFiles.BASHRC.value) as bashrc:
      contents = bashrc.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_MAC.value) as bashInput:
        self.assertTrue(bashInput.read() not in contents)

  def testBashPrivateNotWrittenToBashrcInWorkingDir(self):
    env.platform = Systems.LINUX.value
    bashfile.compileBashrc()
    with open(env.outputFilesDir + BashOutputFiles.BASHRC.value) as bashrc:
      contents = bashrc.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value) as bashInput:
        self.assertTrue(bashInput.read() not in contents)

  def testBashPrivateWrittenToBashrcInHomeDir(self):
    env.platform = Systems.LINUX.value
    bashfile.compileBashrc()
    with open(env.homeDir + BashOutputFiles.DOT_BASHRC.value) as bashrc:
      contents = bashrc.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)

  def testBashPrivateIsSkippedWhenNotPresent(self):
    env.platform = Systems.DARWIN.value
    with open(BashInputFiles.BASH_PRIVATE.value) as bashPrivate:
      bashPrivateText = bashPrivate.read()
    testfilemocks.destroyFile(BashInputFiles.BASH_PRIVATE.value)
    bashfile.compileBashProfile()
    self.assertTrue(BashInputFiles.BASH_PRIVATE.value + " is not present. Skipping..." in sys.stdout.getvalue().strip())
    testfilemocks.createFile(BashInputFiles.BASH_PRIVATE.value, bashPrivateText)

  def testScriptsDirIsWrittenToBashFile(self):
    env.platform = Systems.DARWIN.value
    bashfile.compileBashProfile()
    with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value) as bash_profile:
      for line in bash_profile.readlines():
        if 'scriptsDir' in line:
          self.assertTrue(os.path.isdir(line.replace('\"',"").replace('\n',"").split('=')[1]))
          return
    self.fail("scriptsDir not written to bash file!")

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
