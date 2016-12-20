#!/usr/bin/python

import sys
import os
import unittest
import argparse

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dotfilesmanager
import testfilemocks
import bashfile
from constants import Systems, BashInputFiles, BashOutputFiles

class BashFileIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dotfilesmanager.init()
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

    def testBashLocalNotWrittenToBashProfileInWorkingDir(self):
        env.platform = Systems.DARWIN.value
        bashfile.compileBashProfile()
        with open(env.outputFilesDir + BashOutputFiles.BASH_PROFILE.value) as bashProfile:
            contents = bashProfile.read()
            with open(env.inputFilesDir + BashInputFiles.BASH_LOCAL.value) as bashInput:
                self.assertTrue(bashInput.read() not in contents)

    def testBashLocalWrittenToBashProfileInHomeDir(self):
        env.platform = Systems.DARWIN.value
        bashfile.compileBashProfile()
        with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value) as bashProfile:
            contents = bashProfile.read()
            with open(env.inputFilesDir + BashInputFiles.BASH_LOCAL.value) as bashInput:
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

    def testBashLocalWrittenToBashrc(self):
        env.platform = Systems.LINUX.value
        bashfile.compileBashrc()
        with open(env.homeDir + BashOutputFiles.DOT_BASHRC.value) as bashrc:
            contents = bashrc.read()
            with open(env.inputFilesDir + BashInputFiles.BASH_LOCAL.value) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashLocalNotWrittenToBashrcWhenUserPassesArg_no_local(self):
        testenv.setUp()
        env.platform = Systems.LINUX.value
        env.args = env.parser.parse_args(['--no-local'])
        bashfile.compileBashrc()
        with open(env.outputFilesDir + BashOutputFiles.BASHRC.value) as bashrc:
            contents = bashrc.read()
            with open(env.inputFilesDir + BashInputFiles.BASH_LOCAL.value) as bashInput:
                self.assertTrue(bashInput.read() not in contents)

    def testInputFileIsSkippedWhenNotPresent(self):
        env.platform = Systems.DARWIN.value
        env.args = env.parser.parse_args(['-v'])
        with open(env.inputFilesDir + BashInputFiles.BASH_LOCAL.value) as bashLocal:
            bashLocalText = bashLocal.read()
        testfilemocks.destroyFile(env.inputFilesDir + BashInputFiles.BASH_LOCAL.value)
        bashfile.compileBashProfile()
        self.assertTrue(BashInputFiles.BASH_LOCAL.value + " is not present. Skipping..." in sys.stdout.getvalue().strip())
        testfilemocks.createFile(env.inputFilesDir + BashInputFiles.BASH_LOCAL.value, bashLocalText)

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
