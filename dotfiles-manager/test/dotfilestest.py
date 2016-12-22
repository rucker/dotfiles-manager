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
import env
import testenv
import testfilemocks
import ioutils
import methodstubs

class DotfilesTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dotfilesmanager.init()
        self.wasCalled = False
        dotfilesmanager.setArgs()

    def tearDown(self):
        testenv.clearArgs()

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
    def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
        dotfilesmanager.identifySystem()
        self.assertEquals(env.platform, Systems.DARWIN.value)

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
    def testWhenSystemIsLinuxInstallerIdentifiesSystemAsLinux(self):
        dotfilesmanager.identifySystem()
        self.assertEquals(env.platform, Systems.LINUX.value)

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.WINDOWS.value))
    def testWhenSystemIsWindowsInstallerIdentifiesSystemAsWindowsAndExitsWithCode1(self):
        with self.assertRaises(SystemExit) as cm:
            dotfilesmanager.identifySystem()
            self.assertTrue(sys.stdout.getvalue().strip().endswith('not supported!'))
            assertEqual(cm.exception.code, 1)

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
    def testWhenSystemIsDarwinAndGNUCoreUtilsAreInstalledThenEnvIsSetCorrectly(self):
        with mock.patch('os.path.isdir', return_value=True):
            dotfilesmanager.identifySystem()
            self.assertTrue(env.isGnu)

    def testWhenUserPassesArg_r_thenCorrectLogicalBranchingOccurs(self):
        env.args = env.parser.parse_args(['-r'])
        dotfilesmanager.setEnv = testenv.setUp
        dotfilesmanager.ioutils.revertDotfiles = methodstubs.methodCalled(self)
        dotfilesmanager.main()
        self.assertTrue(self.wasCalled)

    def testWhenUserPassesArg_o_thenCorrectOutputDirIsStoredInEnv(self):
        env.args = env.parser.parse_args(['-o', 'some_dir'])
        dotfilesmanager.setEnv()
        self.assertTrue(env.outputDir == 'some_dir')

    def testWhenUserPassesArg_i_thenCorrectInputDirIsStoredInEnv(self):
        env.args = env.parser.parse_args(['-i', 'some_dir'])
        dotfilesmanager.setEnv()
        self.assertTrue(env.inputDir == 'some_dir')

    def testWhenInputDirIsNotSetSetEnvWillPrintUsage(self):
        dotfilesmanager.setEnv()
        self.assertTrue("usage:" in sys.stdout.getvalue().strip())

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
