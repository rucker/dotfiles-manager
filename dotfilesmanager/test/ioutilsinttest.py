#!/usr/bin/env python3

import sys
import io
import os
from os.path import join
import shutil
import unittest
from unittest import mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager.test import testenv
from dotfilesmanager.test import testfilemocks
from dotfilesmanager import dfm
from dotfilesmanager import ioutils
from dotfilesmanager.constants import DOTFILES, BASHFILES


class IOUtilsIntTest(unittest.TestCase):
    fileName = BASHFILES.BASH_PROFILE.value
    bakFileName = fileName[fileName.rfind('/') + 1 :].replace('.','')
    gitconfig = '.gitconfig'
    gitconfig_global = 'gitconfig_global'
    gitconfig_local = 'gitconfig_local'

    @classmethod
    def setUpClass(self):
        dfm.env = testenv
        dfm.ioutils.env = testenv
        dfm._set_args()
        testenv.setUp()

    @classmethod
    def tearDownClass(self):
        testenv.tearDown()

    def createBashProfile(self):
        testfilemocks.create_file(join(testenv.OUTPUT_DIR, self.fileName), "some_bash_token=some_value")

    def cleanUpBackups(self):
        shutil.rmtree(testenv.BACKUPS_DIR)
        os.mkdir(testenv.BACKUPS_DIR)

    def testWhenUserDoesNotPassArg_c_andDotfileBeingWrittenAlreadyExistsThenItGetsBackedUp(self):
        self.createBashProfile()
        with io.StringIO() as buf:
            buf.write(str("some_bash_token=some_newer_value"))
            ioutils.write_output_file(join(testenv.OUTPUT_DIR, BASHFILES.BASH_PROFILE.value), buf)
        backup_files = os.listdir(testenv.BACKUPS_DIR)
        self.assertTrue(len(backup_files) is 1)
        with open(join(testenv.BACKUPS_DIR, backup_files[0])) as bakFile:
            self.assertTrue("some_value" in bakFile.read())
        self.cleanUpBackups()

    def testWhenUserPassesArg_r_AndEnters_Y_whenPromptedThenDotfilesAreRestoredToMostRecentBackedUpVersion(self):
        self.createBashProfile()
        ioutils.create_file(join(testenv.BACKUPS_DIR, self.bakFileName + '_2016-07-07_14-40-00.bak'),  "some_bash_token=some_value")
        ioutils.create_file(join(testenv.BACKUPS_DIR, self.bakFileName + '_2016-07-07_14-43-00.bak'), "some_bash_token=some_newer_value")

        with mock.patch('builtins.input', return_value='y'):
            ioutils.revert_dotfiles([self.fileName])
        with open(join(testenv.OUTPUT_DIR, self.fileName)) as bash_profile:
            contents = bash_profile.read()
            self.assertTrue("some_newer_value" in contents)
        self.cleanUpBackups()

    def testWhenUserPassesArg_r_AndEnters_N_whenPromptedThenBackedUpDotfilesAreNotRestored(self):
        self.createBashProfile()
        ioutils.create_file(join(testenv.BACKUPS_DIR, self.bakFileName + '_2016-07-07_14-40-00.bak'), "some_bash_token=some_value")
        ioutils.create_file(join(testenv.BACKUPS_DIR, self.bakFileName + '_2016-07-07_14-43-00.bak'), "some_bash_token=some_newer_value")
        with mock.patch('builtins.input', return_value='n'):
            ioutils.revert_dotfiles([self.fileName])
        with open(join(testenv.OUTPUT_DIR, self.fileName)) as bash_profile:
            self.assertTrue("some_newer_value" not in bash_profile.read())
        self.cleanUpBackups()

    def testWhenUserPassesArg_no_localThenOutputFileDoesNotContainContentsOfLocalInputFile(self):
        testenv.ARGS = testenv.parser.parse_args(['--no-local'])
        ioutils.compile_dotfile(DOTFILES.GITCONFIG.value)
        with open(join(testenv.OUTPUT_DIR, DOTFILES.GITCONFIG.value)) as outputFile:
            with open(join(testenv.INPUT_DIR, self.gitconfig_global)) as inputFile:
                with open(join(testenv.INPUT_DIR, self.gitconfig_local)) as \
                localInputFile:
                    contents = outputFile.read()
                    self.assertTrue(inputFile.read() in contents)
                    self.assertTrue(localInputFile.read() not in contents)

    def testDotfileOutputFileContainsTheContentsOfDotfileAndLocalInputFile(self):
        ioutils.compile_dotfile(DOTFILES.GITCONFIG.value)
        with open(join(testenv.OUTPUT_DIR, DOTFILES.GITCONFIG.value)) as outputFile:
            with open(join(testenv.INPUT_DIR, self.gitconfig_global)) as inputFile:
                with open(join(testenv.INPUT_DIR, self.gitconfig_local)) as \
                localInputFile:
                    contents = outputFile.read()
                    self.assertTrue(inputFile.read() in contents)
                    self.assertTrue(localInputFile.read() in contents)

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
