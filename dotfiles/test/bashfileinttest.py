#!/usr/bin/python

import sys
import unittest

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import dotfiles
import testfilemocks
from dotfiles import bashfile
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
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value) as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_COMMON.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)
      with open(env.inputFilesDir + BashInputFiles.BASH_MAC.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)

  def testBashLinuxNotWrittenToBashProfile(self):
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value) as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_LINUX.value) as bashInput:
        self.assertTrue(bashInput.read() not in contents)

  def testBashPrivateNotWrittenToBashProfileInWorkingDir(self):
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
    bashfile.compileBashrc()
    with open(env.outputFilesDir + BashOutputFiles.BASHRC.value) as bashrc:
      contents = bashrc.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_COMMON.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)
      with open(env.inputFilesDir + BashInputFiles.BASH_LINUX.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)

  def testBashMacNotWrittenToBashrc(self):
    bashfile.compileBashrc()
    with open(env.outputFilesDir + BashOutputFiles.BASHRC.value) as bashrc:
      contents = bashrc.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_MAC.value) as bashInput:
        self.assertTrue(bashInput.read() not in contents)

  def testBashPrivateNotWrittenToBashrcInWorkingDir(self):
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

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
