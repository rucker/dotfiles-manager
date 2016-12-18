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
from constants import Systems, VimFiles
import env
import testenv
import testfilemocks
import ioutils
import methodstubs

class IOUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dotfilesmanager.init()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-v', '--verbose', action='store_true')

    def testWhenDotfilesIsRunWith_v_flagThenOutputIsVerbose(self):
        env.args = self.parser.parse_args(['-v'])
        ioutils.output("Compiling dotfiles!")
        self.assertTrue("Compiling dotfiles!" in sys.stdout.getvalue().strip())

    def testWhenDotfilesIsRunWithout_v_flagThenOutputNotVerbose(self):
        env.args.verbose = False
        ioutils.output("Compiling dotfiles!")
        self.assertFalse("Compiling dotfiles!" in sys.stdout.getvalue().strip())

    def testWhenRequiredInputFileDoesNotExistThenAnErrorIsPrintedAndProgramExitsWithStatus_1(self):
        with self.assertRaises(SystemExit) as cm:
            ioutils.writeRequiredInputFileContents("foo", "bar")
            self.assertTrue(sys.stdout.getvalue().strip().contains("Please replace the file and try again."))
            assertEqual(cm.exception.code, 1)

suite = unittest.TestLoader().loadTestsFromTestCase(IOUtilsTest)
unittest.main(module=__name__, buffer=True, exit=False)
