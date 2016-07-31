#!/usr/bin/python

import sys
import unittest
import mock
import platform
import os
import io
import argparse

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import dotfiles
from constants import Systems, VimFiles
import env
import testenv
import testfilemocks
import ioutils
import methodstubs

class DotfilesTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    dotfiles.init()
    self.wasCalled = False

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
    dotfiles.identifySystem()
    self.assertEquals(env.platform, Systems.DARWIN.value)

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
  def testWhenSystemIsLinuxInstallerIdentifiesSystemAsLinux(self):
    dotfiles.identifySystem()
    self.assertEquals(env.platform, Systems.LINUX.value)

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.WINDOWS.value))
  def testWhenSystemIsWindowsInstallerIdentifiesSystemAsWindowsAndExitsWithCode1(self):
    with self.assertRaises(SystemExit) as cm:
      dotfiles.identifySystem()
      self.assertTrue(sys.stdout.getvalue().strip().endswith('not supported!'))
      assertEqual(cm.exception.code, 1)

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
  def testWhenSystemIsDarwinAndGNUCoreUtilsAreInstalledThenEnvIsSetCorrectly(self):
    with mock.patch('os.path.isdir', return_value=True):
      dotfiles.identifySystem()
      self.assertTrue(env.isGnu)

  def testWhenUserPassesArg_r_thenCorrectLogicalBranchingOccurs(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--revert', action='store_true')
    env.args = parser.parse_args(['-r'])
    dotfiles.setEnv = testenv.setUp
    dotfiles.ioutils.revertDotFiles = methodstubs.methodCalled(self)
    dotfiles.main()
    self.assertTrue(self.wasCalled)

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
