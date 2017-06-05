#!/usr/bin/env python3.6

import sys
import unittest
from unittest import mock
from unittest.mock import ANY
import os
from os.path import join, isfile
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager.test import testenv
from dotfilesmanager import dfm
from dotfilesmanager import ioutils
from dotfilesmanager.constants import BASHFILES

class IOUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dfm.env = testenv
        dfm.ioutils.env = testenv
        dfm._set_args()

    def tearDown(self):
        testenv.clearArgs()

    def testWhenRunWith_v_flagThenOutputIsVerbose(self):
        testenv.ARGS = testenv.parser.parse_args(['-v'])
        ioutils.sprint("Compiling dotfiles!")
        self.assertTrue("Compiling dotfiles!" in sys.stdout.getvalue().strip())
        testenv.ARGS = testenv.parser.parse_args([])

    def testWhenRunWithout_v_flagThenOutputIsNotVerbose(self):
        ioutils.sprint("Compiling dotfiles!")
        self.assertFalse("Compiling dotfiles!" in sys.stdout.getvalue().strip())

    @mock.patch('dotfilesmanager.ioutils.backup_file')
    @mock.patch('dotfilesmanager.ioutils.isfile', return_value=True)
    @mock.patch('builtins.open')
    def testWhenUserDoesNotPassArg_c_andDotfileBeingWrittenAlreadyExistsThenItGetsBackedUp(self, mopen, isfile, backup_file):
        with io.StringIO() as buf:
            ioutils.write_output_file(join(testenv.OUTPUT_DIR, BASHFILES.BASHRC.value), buf)
        backup_file.assert_called_once()

    @mock.patch('os.path.isfile', return_value=True)
    def testCorrectOutputFileNamesAreDerivedFromInputFiles(self, isfile):
        inputFiles = [ 'gitconfig_local', 'vimrc' ]
        dotfileNames = []
        for f in inputFiles:
            dotfileNames.append(ioutils.get_dotfile_name(f))
        self.assertEqual(dotfileNames, [ '.gitconfig', '.vimrc' ])

    @mock.patch('dotfilesmanager.dfm.ioutils.get_dotfiles_map', \
            return_value={'.fooconfig' : ['fooconfig', 'fooconfig_local']})
    @mock.patch('dotfilesmanager.ioutils.write_output_file')
    def testCorrectOutputFileNamesAreWritten(self, write_output_file, get_dotfiles_map):
        ioutils.compile_dotfiles(testenv.INPUT_DIR)
        write_output_file.assert_called_with(join(testenv.OUTPUT_DIR, '.fooconfig'), ANY)

    @mock.patch('os.listdir', return_value=[ 'bash', 'bash_mac_gnu', 'gitconfig', 'vimrc' ])
    @mock.patch('os.path.isfile', return_value=True)
    def testDotfilesMapIsConstructedCorrectly(self, listdir, isfile):
        expected = set({ '.gitconfig' : [ '.gitconfig' ], '.vimrc': [ 'vimrc' ]})
        self.assertEqual(set(ioutils.get_dotfiles_map(testenv.INPUT_DIR)), expected)

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
