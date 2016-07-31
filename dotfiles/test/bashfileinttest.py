#!/usr/bin/python

import sys
import os
import unittest
import argparse

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dotfiles
import testfilemocks
import bashfile
from constants import Systems, BashInputFiles, BashOutputFiles

class BashFileIntTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    dotfiles.init()
    testenv.setUp()

  @classmethod
  def tearDownClass(self):
    testenv.tearDown()

  def testBashCommonAndBashMacWrittenToBashProfile(self):
    env.platform = Systems.DARWIN.value
    bashfile.compileBashProfile()
    with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value) as bashProfile:
      contents = bashProfile.read()
      with open(env.inputFilesDir + BashInputFiles.BASH_COMMON.value) as bashInput:
        self.assertTrue(bashInput.read() in contents)
      with open(env.inputFilesDir + BashInputFiles.BASH_MAC_GNU.value) as bashInput:
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
      with open(env.inputFilesDir + BashInputFiles.BASH_MAC_GNU.value) as bashInput:
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

  def testInputFileIsSkippedWhenNotPresent(self):
    env.platform = Systems.DARWIN.value
    env.args = env.parser.parse_args(['-v'])
    with open(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value) as bashPrivate:
      bashPrivateText = bashPrivate.read()
    testfilemocks.destroyFile(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value)
    bashfile.compileBashProfile()
    self.assertTrue(BashInputFiles.BASH_PRIVATE.value + " is not present. Skipping..." in sys.stdout.getvalue().strip())
    testfilemocks.createFile(env.inputFilesDir + BashInputFiles.BASH_PRIVATE.value, bashPrivateText)

  def testWhenUserPassesArg_c_ThenExistingOutputFilesAreClobbered(self):
    env.args = env.parser.parse_args(['-c'])
    with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value, 'w') as bash_profile:
      bash_profile.write("some_bash_token=some_value")
    bashfile.compileBashProfile()
    self.assertTrue("already exists. Renaming" not in sys.stdout.getvalue().strip())
    self.assertFalse(os.path.isfile(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value + '.bak'))
    env.args = ''

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
