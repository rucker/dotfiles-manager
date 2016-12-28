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

class DotfilesTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dotfilesmanager.env = testenv
        dotfilesmanager.ioutils.env = testenv
        self.wasCalled = False
        dotfilesmanager.setArgs()

    def tearDown(self):
        testenv.clearArgs()

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
    def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
        dotfilesmanager.identifySystem()
        self.assertEquals(testenv.platform, Systems.DARWIN.value)

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
    def testWhenSystemIsLinuxInstallerIdentifiesSystemAsLinux(self):
        dotfilesmanager.identifySystem()
        self.assertEquals(testenv.platform, Systems.LINUX.value)

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.WINDOWS.value))
    def testWhenSystemIsWindowsInstallerIdentifiesSystemAsWindowsAndExitsWithCode1(self):
        with self.assertRaises(SystemExit) as cm:
            dotfilesmanager.identifySystem()
            self.assertTrue(sys.stdout.getvalue().strip().endswith('not supported!'))
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
    def testWhenSystemIsDarwinAndGNUCoreUtilsAreInstalledThenEnvIsSetCorrectly(self):
        with mock.patch('os.path.isdir', return_value=True):
            dotfilesmanager.identifySystem()
            self.assertTrue(testenv.isGnu)

    @mock.patch('dotfilesmanager.setArgs')
    @mock.patch('dotfilesmanager.ioutils.revertDotfiles')
    def testWhenUserPassesArg_r_thenCorrectLogicalBranchingOccurs(self, setArgs, revertDotFiles):
        testenv.args = testenv.parser.parse_args(['-r'])
        setArgs.side_effect = methodstubs.noop(self)
        revertDotFiles.side_effect = methodstubs.methodCalled(self)
        dotfilesmanager.main()
        self.assertTrue(self.wasCalled)

    def testWhenUserPassesArg_o_thenCorrectOutputDirIsStoredInEnv(self):
        testenv.args = testenv.parser.parse_args(['-o', 'some_dir'])
        dotfilesmanager.setEnv()
        self.assertTrue(testenv.outputDir == 'some_dir')

    def testWhenUserPassesArg_i_thenSpecifiedInputDirIsStoredInEnv(self):
        testenv.args = testenv.parser.parse_args(['-i', 'some_dir'])
        dotfilesmanager.setEnv()
        self.assertTrue(testenv.inputDir == 'some_dir/')

#    def testWhenInputDirIsNotSetSetEnvPrintsUsageAndExitsWithCode1(self):
#        with self.assertRaises(SystemExit) as cm:
#            dotfilesmanager.setEnv()
#            self.assertTrue("usage:" in sys.stdout.getvalue().strip())
#        self.assertEqual(cm.exception.code, 1)

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
