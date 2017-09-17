#!/usr/bin/env python3.6

import sys
import unittest
from unittest import mock
from unittest.mock import call
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager import dfm, ioutils
from dotfilesmanager.constants import SYSTEMS, BASHFILES
from dotfilesmanager.test import testenv

class DotfilesManagerTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dfm.env = testenv
        dfm.ioutils.env = testenv
        dfm._set_args()

    def tearDown(self):
        testenv.clearArgs()

    @mock.patch('platform.system', mock.MagicMock(return_value=SYSTEMS.DARWIN.value))
    def testDarwinSystemsIdentifiedCorreectly(self):
        dfm._identify_system()
        self.assertEqual(testenv.PLATFORM, SYSTEMS.DARWIN.value)

    @mock.patch('platform.system', mock.MagicMock(return_value=SYSTEMS.LINUX.value))
    def testLinuxSystemsIdentifiedCorrectly(self):
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

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils.get_dotfiles_map', \
            return_value={'.fooconfig' : ['fooconfig', 'fooconfig_local'], '.barconfig' : ['barconfig']})
    @mock.patch('dotfilesmanager.dfm.ioutils', autospec=True)
    @mock.patch('dotfilesmanager.dfm.bashfile', autospec=True)
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_r_thenCorrectLogicalBranchingOccurs(self, isdir, bashfile, ioutils, get_dotfiles_map, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['some_dir', '-r'])
        dfm.main()
        ioutils.get_dotfiles_map.assert_called_with(testenv.INPUT_DIR)
        ioutils.revert_dotfiles.assert_called_with(['.fooconfig', '.barconfig', BASHFILES.BASHRC.value])

    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_o_thenCorrectOutputDirIsStoredInEnv(self, isdir):
        testenv.ARGS = testenv.parser.parse_args(['some_dir', '-o', 'some_dir'])
        dfm._set_env()
        self.assertTrue(testenv.OUTPUT_DIR == 'some_dir')

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_f_bashrc_thenOnlyTheSpecifiedFileIsCompiled(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['some_dir', '-f', '.bashrc'])
        dfm.main()
        bashfile.compile_bashrc.assert_called_once()
        ioutils.compile_dotfile.assert_not_called()

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArg_f_bash_profile_thenOnlyTheSpecifiedFileIsCompiled(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['some_dir', '-f', '.bash_profile'])
        dfm.main()
        bashfile.compile_bash_profile.assert_called_once()
        bashfile.compile_bashrc.assert_not_called()
        ioutils.compile_dotfile.assert_not_called()

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils.compile_dotfile')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dotfilesmanager.dfm.ioutils.get_dotfiles_map', return_value={'.gitconfig' : ['gitconfig', 'gitconfig_local']})
    def testWhenUserPassesArg_f_gitconfig_thenOnlyTheSpecifiedFileIsCompiled(self, get_dotfiles_map, isdir, bashfile, compile_dotfile, _set_args):
        dotfile = '.gitconfig'
        testenv.ARGS = testenv.parser.parse_args(['some_dir', '-f', dotfile])
        dfm.main()
        bashfile.compile_bashrc.assert_not_called()
        bashfile.compile_bash_profile.assert_not_called()
        ioutils.compile_dotfile.assert_called_once()
        ioutils.compile_dotfile.assert_called_with(dotfile)

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('dotfilesmanager.dfm.ioutils.get_dotfiles_map', return_value={'.gitconfig' : ['gitconfig', 'gitconfig_local']})
    def testWhenUserPassesArg_f_andAnInvalidDotfileNameThenPrintAWarningAndExit(self, get_dotfiles_map, isdir, _set_args):
        dfm.env.ARGS = testenv.parser.parse_args(['some_dir', '-v', '-f', 'foobar'])
        with self.assertRaises(SystemExit) as se:
            dfm.main()
        self.assertEqual(se.exception.code, 0)
        self.assertTrue("No input files found" in sys.stderr.getvalue())

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=True)
    def testWhenUserPassesArgs_rf_thenOnlyTheSpecifiedFileIsReverted(self, isdir, bashfile, ioutils, _set_args):
        testenv.ARGS = testenv.parser.parse_args(['some_dir', '-r', '-f', '.bash_profile'])
        dfm.main()
        ioutils.revert_dotfile.assert_called_with(BASHFILES.BASH_PROFILE.value)
        bashfile.compile_bashrc.assert_not_called()
        bashfile.compile_bash_profile.assert_not_called()
        ioutils.compile_dotfile.assert_not_called()

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.dfm.ioutils')
    @mock.patch('dotfilesmanager.dfm.bashfile')
    @mock.patch('os.path.isdir', return_value=False)
    def testWhenUserSpecifiesNonExistentInputDirThenPrintAnErrorAndExitWithCode1(self, isdir, bashfile, ioutils, _set_args):
        input_dir = 'some_nonexistent_dir'
        testenv.ARGS = testenv.parser.parse_args(['-r', input_dir])
        with self.assertRaises(SystemExit) as se:
            dfm._set_env()
        self.assertEqual(se.exception.code, 1)
        self.assertTrue("Specified input directory " + input_dir + " does not exist." in sys.stderr.getvalue())

    @mock.patch('dotfilesmanager.dfm._set_args')
    @mock.patch('dotfilesmanager.bashfile.compile_bash_file')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.listdir', return_value=['foorc', 'foorc_local', 'bar.config'])
    @mock.patch('dotfilesmanager.ioutils.compile_dotfile')
    def testArbitraryDotfilesAreCompiledAccordingToInputFileNameConvention(self, compile_dotfile, listdir, isfile, isdir, compile_bash_file, set_args):
        testenv.ARGS = testenv.parser.parse_args(['some_dir'])
        dfm.main()
        expectedCalls = [ call('.foorc'), call('.bar.config') ]
        ioutils.compile_dotfile.assert_has_calls(expectedCalls)

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
