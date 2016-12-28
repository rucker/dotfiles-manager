#!/usr/bin/python

import sys
import os
import unittest
import argparse

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import testenv
import dotfilesmanager
import testfilemocks
import bashfile
from constants import Systems, Srcfiles, Dotfiles

class BashFileIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dotfilesmanager.env = testenv
        dotfilesmanager.ioutils.env = testenv
        dotfilesmanager.bashfile.env = testenv
        dotfilesmanager.identifySystem()
        dotfilesmanager.setArgs()
        testenv.setUp()

    @classmethod
    def tearDownClass(self):
        testenv.tearDown()

    def tearDown(self):
        testenv.clearArgs()

    def testBashCommonAndBashMacWrittenToBashProfile(self):
        testenv.platform = Systems.DARWIN.value
        bashfile.compileBashProfile()
        with open(testenv.outputDir + Dotfiles.BASH_PROFILE.value) as bashProfile:
            contents = bashProfile.read()
            with open(testenv.inputDir + Srcfiles.BASH_COMMON.value) as bashInput:
                self.assertTrue(bashInput.read() in contents)
            with open(testenv.inputDir + Srcfiles.BASH_MAC_GNU.value) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashLinuxNotWrittenToBashProfile(self):
        testenv.platform = Systems.DARWIN.value
        bashfile.compileBashProfile()
        with open(testenv.outputDir + Dotfiles.BASH_PROFILE.value) as bashProfile:
            contents = bashProfile.read()
            with open(testenv.inputDir + Srcfiles.BASH_LINUX.value) as bashInput:
                self.assertTrue(bashInput.read() not in contents)

    def testBashLocalWrittenToBashProfileWhenArg_no_local_notPassed(self):
        testenv.platform = Systems.DARWIN.value
        bashfile.compileBashProfile()
        with open(testenv.outputDir + Dotfiles.BASH_PROFILE.value) as bashProfile:
            contents = bashProfile.read()
            with open(testenv.inputDir + Srcfiles.BASH_LOCAL.value) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashCommonAndBashLinuxWrittenToBashrc(self):
        testenv.platform = Systems.LINUX.value
        bashfile.compileBashrc()
        with open(testenv.outputDir + Dotfiles.BASHRC.value) as bashrc:
            contents = bashrc.read()
            with open(testenv.inputDir + Srcfiles.BASH_COMMON.value) as bashInput:
                self.assertTrue(bashInput.read() in contents)
            with open(testenv.inputDir + Srcfiles.BASH_LINUX.value) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashMacNotWrittenToBashrc(self):
        testenv.platform = Systems.LINUX.value
        bashfile.compileBashrc()
        with open(testenv.outputDir + Dotfiles.BASHRC.value) as bashrc:
            contents = bashrc.read()
            with open(testenv.inputDir + Srcfiles.BASH_MAC_GNU.value) as bashInput:
                self.assertTrue(bashInput.read() not in contents)

    def testBashLocalWrittenToBashrc(self):
        testenv.platform = Systems.LINUX.value
        bashfile.compileBashrc()
        with open(testenv.outputDir + Dotfiles.BASHRC.value) as bashrc:
            contents = bashrc.read()
            with open(testenv.inputDir + Srcfiles.BASH_LOCAL.value) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashLocalNotWrittenToBashrcWhenUserPassesArg_no_local(self):
        testenv.setUp()
        testenv.platform = Systems.LINUX.value
        args = testenv.args
        testenv.args = testenv.parser.parse_args(['--no-local'])

        bashfile.compileBashrc()
        with open(testenv.outputDir + Dotfiles.BASHRC.value) as bashrc:
            contents = bashrc.read()
            with open(testenv.inputDir + Srcfiles.BASH_LOCAL.value) as bashInput:
                self.assertTrue(bashInput.read() not in contents)

        testenv.args = args

    def testInputFileIsSkippedWhenNotPresent(self):
        testenv.platform = Systems.DARWIN.value
        args = testenv.args
        testenv.args = testenv.parser.parse_args(['-v'])

        with open(testenv.inputDir + Srcfiles.BASH_LOCAL.value) as bashLocal:
            bashLocalText = bashLocal.read()
        testfilemocks.destroyFile(testenv.inputDir + Srcfiles.BASH_LOCAL.value)
        bashfile.compileBashProfile()
        self.assertTrue(Srcfiles.BASH_LOCAL.value + " is not present. Skipping..." in sys.stdout.getvalue().strip())
        testfilemocks.createFile(testenv.inputDir + Srcfiles.BASH_LOCAL.value, bashLocalText)

        testenv.args = args

    def testWhenUserPassesArg_c_ThenExistingOutputFilesAreClobbered(self):
        testenv.args = testenv.parser.parse_args(['-c'])
        with open(testenv.outputDir + Dotfiles.BASH_PROFILE.value, 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_value")
        bashfile.compileBashProfile()
        self.assertTrue("already exists. Renaming" not in sys.stdout.getvalue().strip())
        self.assertFalse(os.path.isfile(testenv.outputDir + Dotfiles.BASH_PROFILE.value + '.bak'))
        testenv.args = ''

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
