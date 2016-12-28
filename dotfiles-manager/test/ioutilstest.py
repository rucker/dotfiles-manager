#!/usr/bin/python

import sys
import unittest
import mock
import platform
import os
import io
import argparse

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import dotfilesmanager
from constants import Systems, Dotfiles
import testenv
import testfilemocks
import ioutils
import methodstubs

class IOUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dotfilesmanager.env = testenv
        dotfilesmanager.ioutils.env = testenv
        dotfilesmanager.setArgs()

    def tearDown(self):
        testenv.clearArgs()

    def testWhenDotfilesIsRunWith_v_flagThenOutputIsVerbose(self):
        testenv.args = testenv.parser.parse_args(['-v'])
        ioutils.output("Compiling dotfiles!")
        self.assertTrue("Compiling dotfiles!" in sys.stdout.getvalue().strip())
        testenv.args = testenv.parser.parse_args([])

    def testWhenDotfilesIsRunWithout_v_flagThenOutputNotVerbose(self):
        ioutils.output("Compiling dotfiles!")
        self.assertFalse("Compiling dotfiles!" in sys.stdout.getvalue().strip())

    def testWhenRequiredInputFileDoesNotExistThenAnErrorIsPrintedAndProgramExitsWithStatus_1(self):
        with self.assertRaises(SystemExit) as cm:
            ioutils.writeRequiredInputFileContents("foo", "bar")
            self.assertTrue(sys.stdout.getvalue().strip().contains("Please replace the file and try again."))
        self.assertEqual(cm.exception.code, 1)

suite = unittest.TestLoader().loadTestsFromTestCase(IOUtilsTest)
unittest.main(module=__name__, buffer=True, exit=False)
