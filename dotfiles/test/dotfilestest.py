#!/usr/bin/python

import sys
sys.path.insert(0, '../')
import unittest
import mock
import platform
import os
import io
import time

import dotfiles
from constants import Systems
import env

class DotfilesTest(unittest.TestCase):

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
    dotfiles.identifySystem()
    self.assertTrue(sys.stdout.getvalue().strip().endswith(Systems.DARWIN.value))

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
  def testWhenSystemIsLinuxInstallerIdentifiesSystemAsLinux(self):
    dotfiles.identifySystem()
    self.assertTrue(sys.stdout.getvalue().strip().endswith(Systems.LINUX.value))

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.WINDOWS.value))
  def testWhenSystemIsWindowsInstallerIdentifiesSystemAsWindowsAndExitsWithCode1(self):
    with self.assertRaises(SystemExit) as cm:
      dotfiles.identifySystem()
      self.assertTrue(sys.stdout.getvalue().strip().endswith('not supported!'))
      assertEqual(cm.exception.code, 1)

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
