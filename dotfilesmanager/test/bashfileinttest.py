#!/usr/bin/env python

import sys
import os
from os.path import join
import unittest
import argparse
import mock

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import testenv
import dfm
import testfilemocks
import bashfile
from constants import SYSTEMS, SRCFILES, DOTFILES
import ioutils

class BashFileIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dfm.env = testenv
        dfm.ioutils.env = testenv
        dfm.bashfile.env = testenv
        dfm._identify_system()
        dfm._set_args()
        testenv.setUp()

    def setUp(self):
        testenv.setUp()

    def tearDown(self):
        testenv.tearDown()
        testenv.clearArgs()

    def testBashGlobalAndBashMacWrittenToBashProfile(self):
        bashfile.compile_bash_file(SYSTEMS.DARWIN.value)
        with open(join(testenv.OUTPUT_DIR, DOTFILES.BASH_PROFILE.value)) as bashProfile:
            contents = bashProfile.read()
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_GLOBAL.value)) as bashInput:
                self.assertTrue(bashInput.read() in contents)
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_MAC_GNU.value)) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashLinuxNotWrittenToBashProfile(self):
        bashfile.compile_bash_file(SYSTEMS.DARWIN.value)
        with open(join(testenv.OUTPUT_DIR, DOTFILES.BASH_PROFILE.value)) as bashProfile:
            contents = bashProfile.read()
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_LINUX.value)) as bashInput:
                self.assertTrue(bashInput.read() not in contents)

    def testBashLocalWrittenToBashProfileWhenArg_no_local_notPassed(self):
        bashfile.compile_bash_profile()
        with open(join(testenv.OUTPUT_DIR, DOTFILES.BASH_PROFILE.value)) as bashProfile:
            contents = bashProfile.read()
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_LOCAL.value)) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashGlobalAndBashLinuxWrittenToBashrc(self):
        bashfile.compile_bash_file(SYSTEMS.LINUX.value)
        with open(join(testenv.OUTPUT_DIR, DOTFILES.BASHRC.value)) as bashrc:
            contents = bashrc.read()
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_GLOBAL.value)) as bashInput:
                self.assertTrue(bashInput.read() in contents)
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_LINUX.value)) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashMacContentNotWrittenToBashrc(self):
        bashfile.compile_bash_file(SYSTEMS.LINUX.value)
        with open(join(testenv.OUTPUT_DIR, DOTFILES.BASHRC.value)) as bashrc:
            contents = bashrc.read()
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_MAC_GNU.value)) as bashInput:
                self.assertTrue(bashInput.read() not in contents)
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_MAC_BSD.value)) as bashInput:
                self.assertTrue(bashInput.read() not in contents)

    def testBashLocalWrittenToBashrc(self):
        bashfile.compile_bash_file(SYSTEMS.LINUX.value)
        with open(join(testenv.OUTPUT_DIR, DOTFILES.BASHRC.value)) as bashrc:
            contents = bashrc.read()
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_LOCAL.value)) as bashInput:
                self.assertTrue(bashInput.read() in contents)

    def testBashLocalNotWrittenToBashrcWhenUserPassesArg_no_local(self):
        testenv.setUp()
        args = testenv.ARGS
        testenv.ARGS = testenv.parser.parse_args(['--no-local'])

        bashfile.compile_bash_file(SYSTEMS.LINUX.value)
        with open(join(testenv.OUTPUT_DIR, DOTFILES.BASHRC.value)) as bashrc:
            contents = bashrc.read()
            with open(join(testenv.INPUT_DIR, SRCFILES.BASH_LOCAL.value)) as bashInput:
                self.assertTrue(bashInput.read() not in contents)

        testenv.ARGS = args

    def testInputFileIsSkippedWhenNotPresent(self):
        args = testenv.ARGS
        testenv.ARGS = testenv.parser.parse_args(['-v'])

        with open(join(testenv.INPUT_DIR, SRCFILES.BASH_LOCAL.value)) as bashLocal:
            bashLocalText = bashLocal.read()
        ioutils.destroy_file(join(testenv.INPUT_DIR, SRCFILES.BASH_LOCAL.value))
        bashfile.compile_bash_file(SYSTEMS.DARWIN.value)
        self.assertTrue(SRCFILES.BASH_LOCAL.value + " is not present. Skipping..." in sys.stdout.getvalue().strip())
        testfilemocks.create_file(join(testenv.INPUT_DIR, SRCFILES.BASH_LOCAL.value), bashLocalText)

        testenv.ARGS = args

    def testWhenUserPassesArg_c_ThenExistingOutputFilesAreClobbered(self):
        testenv.ARGS = testenv.parser.parse_args(['-c'])
        with open(join(testenv.OUTPUT_DIR, DOTFILES.BASH_PROFILE.value), 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_value")
        bashfile.compile_bash_profile()
        self.assertTrue("already exists. Renaming" not in sys.stdout.getvalue().strip())
        self.assertFalse(os.path.isfile(join(testenv.OUTPUT_DIR, DOTFILES.BASH_PROFILE.value + '.bak')))
        testenv.ARGS = ''

    def testBashProfileNotCreatedInHomeDirOnLinuxSystem(self):
        bashfile.compile_bash_file(SYSTEMS.LINUX.value)
        self.assertFalse(os.path.isfile(join(testenv.OUTPUT_DIR, DOTFILES.BASH_PROFILE.value)))
        self.assertTrue(os.path.isfile(join(testenv.OUTPUT_DIR, DOTFILES.BASHRC.value)))

    def testBashrcNotCreatedInHomeDirOnDarwinSystem(self):
        bashfile.compile_bash_file(SYSTEMS.DARWIN.value)
        self.assertTrue(os.path.isfile(join(testenv.OUTPUT_DIR, DOTFILES.BASH_PROFILE.value)))
        self.assertFalse(os.path.isfile(join(testenv.OUTPUT_DIR, DOTFILES.BASHRC.value)))

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
