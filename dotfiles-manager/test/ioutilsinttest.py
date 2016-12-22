#!/usr/bin/python

import sys
import os
import unittest
import mock

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dotfilesmanager
import ioutils
import testfilemocks
from constants import Systems, Srcfiles, Dotfiles

class IOUtilsIntTest(unittest.TestCase):
    fileName = Dotfiles.BASH_PROFILE.value
    bakFileName = fileName[fileName.rfind('/') + 1 :].replace('.','')

    @classmethod
    def setUpClass(self):
        dotfilesmanager.init()
        testenv.setUp()

    @classmethod
    def tearDownClass(self):
        testenv.tearDown()

    def testWhenUserPassesArg_r_AndEnters_Y_whenPromptedThenDotfilesAreRestoredToMostRecentBackedUpVersion(self):
        with open(env.outputDir + self.fileName, 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_alternate_value")
        with open(env.backupsDir + self.bakFileName + '_2016-07-07_14-40-00.bak', 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_alternate_value")
        with open(env.backupsDir + self.bakFileName + '_2016-07-07_14-43-00.bak', 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_newer_alternate_value")
        with mock.patch('__builtin__.raw_input', return_value='y'):
            ioutils.revertDotfiles([self.fileName])
        with open(env.outputDir + self.fileName) as bash_profile:
            contents = bash_profile.read()
            self.assertTrue("some_newer_alternate_value" in contents)

    def testWhenUserPassesArg_r_AndEnters_N_whenPromptedThenBackedUpDotfilesAreNotRestored(self):
        with open(env.outputDir + self.fileName, 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_alternate_value")
        with open(env.backupsDir + self.bakFileName + '_2016-07-07_14-40-00.bak', 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_alternate_value")
        with open(env.backupsDir + self.bakFileName + '_2016-07-07_14-43-00.bak', 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_newer_alternate_value")
        with mock.patch('__builtin__.raw_input', return_value='n'):
            ioutils.revertDotfiles([self.fileName])
        with open(env.outputDir + self.fileName) as bash_profile:
            self.assertTrue("some_newer_alternate_value" not in bash_profile.read())

    def testWhenUserPassesArg_no_localThenOutputFileDoesNotContainContentsOfLocalInputFile(self):
        env.args = env.parser.parse_args(['--no-local'])
        ioutils.compileDotfile(Dotfiles.GITCONFIG.value)
        with open(env.outputDir + Dotfiles.GITCONFIG.value) as outputFile:
            with open(env.inputDir + Srcfiles.GITCONFIG.value) as inputFile:
                with open(env.inputDir + Srcfiles.GITCONFIG_LOCAL.value) as \
                localInputFile:
                    contents = outputFile.read()
                    self.assertTrue(inputFile.read() in contents)
                    self.assertTrue(localInputFile.read() not in contents)

    def testDotfileOutputFileContainsTheContentsOfDotfileAndLocalInputFile(self):
        ioutils.compileDotfile(Dotfiles.GITCONFIG.value)
        with open(env.outputDir + Dotfiles.GITCONFIG.value) as outputFile:
            with open(env.inputDir + Srcfiles.GITCONFIG.value) as inputFile:
                with open(env.inputDir + Srcfiles.GITCONFIG_LOCAL.value) as \
                localInputFile:
                    contents = outputFile.read()
                    self.assertTrue(inputFile.read() in contents)
                    self.assertTrue(localInputFile.read() in contents)

suite = unittest.TestLoader().loadTestsFromTestCase(IOUtilsIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
