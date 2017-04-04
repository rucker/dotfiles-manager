#!/usr/bin/env python3

import sys
import unittest
from unittest import mock
import platform
import os
import io
import argparse
import builtins

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager import dfm
from dotfilesmanager import ioutils
from dotfilesmanager.constants import SYSTEMS, DOTFILES
from dotfilesmanager.test import testenv
from dotfilesmanager.test import testfilemocks

class DotfilesManagerTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dfm.env = testenv
        dfm.ioutils.env = testenv
        dfm._set_args()

    def tearDown(self):
        testenv.clearArgs()

    @mock.patch('platform.system', mock.MagicMock(return_value=SYSTEMS.DARWIN.value))
    def testDarwinSYSTEMSIdentifiedCorreectly(self):
        dfm._identify_system()
        self.assertEqual(testenv.PLATFORM, SYSTEMS.DARWIN.value)

    @mock.patch('platform.system', mock.MagicMock(return_value=SYSTEMS.LINUX.value))
    def testLinuxSYSTEMSIdentifiedCorrectly(self):
        dfm._identify_system()
        self.assertEqual(testenv.PLATFORM, SYSTEMS.LINUX.value)

    @mock.patch('platform.system', mock.MagicMock(return_value=SYSTEMS.WINDOWS.value))
    def testWhenSystemIsWindowsThenSystemIdentifiedAsWindowsAndExitWithCode1(self):
        with self.assertRaises(SystemExit) as cm:
            dfm._identify_system()
        self.assertTrue(sys.stderr.getvalue().strip().endswith('not supported!'))
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('platform.system', mock.MagicMock(return_value=SYSTEMS.DARWIN.value))
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenSystemIsDarwinAndGNUCoreUtilsAreInstalledThenEnvIsSetCorrectly(self, isdir):
        dfm._identify_system()
        self.assertTrue(testenv.IS_GNU)

    @mock.patch('builtins.open')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_i_thenSpecifiedInputDirIsStoredInEnvAndConfigFileIsNotRead(self, isdir, mopen):
        testenv.ARGS = testenv.parser.parse_args(['-i', 'some_dir'])
        dfm._set_env()
        self.assertTrue(testenv.INPUT_DIR == 'some_dir')
        mopen.assert_not_called()

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils', autospec=True)
    @mock.patch('dotfilesmanager.dfm.bashfile', autospec=True)
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_r_thenCorrectLogicalBranchingOccurs(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['-i', 'some_dir', '-r'])
        dfm.main()
        ioutils.revert_dotfiles.assert_called_with([ df.value for df in DOTFILES ])
        bashfile.compile_bash_files.assert_not_called()

    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_o_thenCorrectOutputDirIsStoredInEnv(self, isdir):
        testenv.ARGS = testenv.parser.parse_args(['-i', 'some_dir', '-o', 'some_dir'])
        dfm._set_env()
        self.assertTrue(testenv.OUTPUT_DIR == 'some_dir')

    @mock.patch('argparse.ArgumentParser.print_help')
    def testWhenInputDirIsNotSetSetEnvPrintsErrorMessageAndUsageAndExitsWithCode1(self, print_help):
        dfm._identify_system()
        with self.assertRaises(SystemExit) as se:
            dfm._set_env()
        self.assertTrue("Please specify input files directory" in sys.stderr.getvalue())
        self.assertEqual(se.exception.code, 1)
        print_help.assert_called_once()

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_f_bashrc_thenOnlyTheSpecifiedFileIsCompiled(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['-i', 'some_dir', '-f', '.bashrc'])
        dfm.main()
        bashfile.compile_bashrc.assert_called_once()
        ioutils.compile_dotfile.assert_not_called()

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_f_bash_profile_thenOnlyTheSpecifiedFileIsCompiled(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['-i', 'some_dir', '-f', '.bash_profile'])
        dfm.main()
        bashfile.compile_bash_profile.assert_called_once()
        bashfile.compile_bashrc.assert_not_called()
        ioutils.compile_dotfile.assert_not_called()

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_f_vimrc_thenOnlyTheSpecifiedFileIsCompiled(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['-i', 'some_dir', '-f', '.vimrc'])
        dfm.main()
        bashfile.compile_bashrc.assert_not_called()
        bashfile.compile_bash_profile.assert_not_called()
        ioutils.compile_dotfile.assert_called_with(DOTFILES.VIMRC.value)

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_f_gitconfig_thenOnlyTheSpecifiedFileIsCompiled(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['-i', 'some_dir', '-f', '.gitconfig'])
        dfm.main()
        bashfile.compile_bashrc.assert_not_called()
        bashfile.compile_bash_profile.assert_not_called()
        ioutils.compile_dotfile.assert_called_with(DOTFILES.GITCONFIG.value)

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_f_andAnInvalidDotfileNameThenPrintAnErrorAndExitWithCode1(self, isdir, _set_args):
        dfm.env.ARGS = testenv.parser.parse_args(['-i', 'some_dir', '-f', 'foobar'])
        with self.assertRaises(SystemExit) as se:
            dfm.main()
        self.assertEqual(se.exception.code, 1)
        self.assertTrue("Valid dotfile names are:" in sys.stderr.getvalue())

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArgs_rf_thenOnlyTheSpecifiedFileIsReverted(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['-i', 'some_dir', '-r', '-f', '.bash_profile'])
        dfm.main()
        ioutils.revert_dotfile.assert_called_with(DOTFILES.BASH_PROFILE.value)
        bashfile.compile_bash_files.assert_not_called()
        bashfile.compile_bashrc.assert_not_called()
        bashfile.compile_bash_profile.assert_not_called()
        ioutils.compile_dotfile.assert_not_called()

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=False)
    def testWhenUserSpecifiesNonExistentInputDirThenPrintAnErrorAndExitWithCode1(self, isdir, bashfile, ioutils, _set_args):
        input_dir = 'some_nonexistent_dir'
        testenv.ARGS = testenv.parser.parse_args(['-r', '-i', input_dir])
        with self.assertRaises(SystemExit) as se:
            dfm._set_env()
        self.assertEqual(se.exception.code, 1)
        self.assertTrue("Specified input directory " + input_dir + " does not exist." in sys.stderr.getvalue())

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
