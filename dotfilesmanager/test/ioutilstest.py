#!/usr/bin/env python3

import sys
import unittest
from unittest import mock
import os
from os.path import join
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager.test import testenv
from dotfilesmanager import dfm
from dotfilesmanager import ioutils
from dotfilesmanager.constants import DOTFILES

class IOUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dfm.env = testenv
        dfm.ioutils.env = testenv
        dfm._set_args()

    def tearDown(self):
        testenv.clearArgs()

    def testWhenDOTFILESIsRunWith_v_flagThenOutputIsVerbose(self):
        testenv.ARGS = testenv.parser.parse_args(['-v'])
        ioutils.sprint("Compiling dotfiles!")
        self.assertTrue("Compiling dotfiles!" in sys.stdout.getvalue().strip())
        testenv.ARGS = testenv.parser.parse_args([])

    def testWhenDOTFILESIsRunWithout_v_flagThenOutputIsNotVerbose(self):
        ioutils.sprint("Compiling dotfiles!")
        self.assertFalse("Compiling dotfiles!" in sys.stdout.getvalue().strip())

    def testWhenRequiredInputFileDoesNotExistThenAnErrorIsPrintedAndProgramExitsWithStatus_1(self):
        with self.assertRaises(SystemExit) as cm:
            ioutils.write_required_input_file_contents("foo", "bar")
        self.assertTrue("Please replace the file and try again." in sys.stderr.getvalue().strip())
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('dotfilesmanager.ioutils.backup_file')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.open')
    def testWhenUserDoesNotPassArg_c_andDotfileBeingWrittenAlreadyExistsThenItGetsBackedUp(self, mopen, isfile, backup_file):
        with io.StringIO() as buf:
            ioutils.write_output_file(join(testenv.OUTPUT_DIR, DOTFILES.BASHRC.value), buf)
        backup_file.assert_called_once()

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
