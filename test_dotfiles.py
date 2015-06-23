#!/usr/bin/python

import unittest
import mock
import dotfilesinstaller
import platform
import sys
import os

class DotfilesTest(unittest.TestCase):
  def setUp(self):
    dotfilesinstaller.init()

  @mock.patch('platform.system', mock.MagicMock(return_value='Darwin'))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
    dotfilesinstaller.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith('Darwin'))

  @mock.patch('platform.system', mock.MagicMock(return_value='Linux'))
  def testWhenSystemIsLinuxInstallerIdentifiesSystemAsLinux(self):
    dotfilesinstaller.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith('Linux'))

  @mock.patch('platform.system', mock.MagicMock(return_value='Windows'))
  def testWhenSystemIsWindowsInstallerIdentifiesSystemAsWindowsAndExits(self):
    with self.assertRaises(SystemExit) as cm:
      dotfilesinstaller.identifySystem()
      assert(sys.stdout.getvalue().strip().endswith('not supported!'))
      assertEqual(cm.exception.code, 1)

  def testWhenBashrcExistsInstallerWillDeleteIt(self):
    if not os.path.isfile('bashrc'):
      testbashrc = open('bashrc','w')
      testbashrc.write('Test file...')
      testbashrc.close()
    dotfilesinstaller.cleanUp()
    assert(sys.stdout.getvalue().strip().endswith('bashrc'))
    self.assertFalse(os.path.isfile('bashrc'))

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
