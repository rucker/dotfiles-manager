#!/usr/bin/python

import sys
import unittest
import mock
import platform
import os
import io
import time

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import dotfiles
from constants import Systems, VimFiles
import env
import testfilemocks

class DotfilesTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    dotfiles.init()

  def setUp(self):
    testfilemocks.createInputFiles()

  def tearDown(self):
    testfilemocks.destroyInputAndOutputFiles()

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

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
