#!/usr/bin/python

import sys
sys.path.insert(0, '../')
import unittest
import mock
import platform
import os
import io
import time

from dotfiles import dotfiles
from dotfiles.systems import Systems

class MockFile(io.StringIO):
  name = None
  def __init__(self, name, buffer_ = None):
    super(MockFile, self).__init__(buffer_)
    self.name = name

class DotfilesTest(unittest.TestCase):

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
    dotfiles.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith(Systems.DARWIN.value))

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
    dotfiles.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith(Systems.LINUX.value))

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.WINDOWS.value))
  def testWhenSystemIsWindowsInstallerIdentifiesSystemAsWindowsAndExitsWithCode1(self):
    with self.assertRaises(SystemExit) as cm:
      dotfiles.identifySystem()
      assert(sys.stdout.getvalue().strip().endswith('not supported!'))
      assertEqual(cm.exception.code, 1)

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
