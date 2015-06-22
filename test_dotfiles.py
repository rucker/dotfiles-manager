#!/usr/bin/python

import unittest
import mock
import dotfilesinstaller
import platform

class DotfilesTest(unittest.TestCase):
  @mock.patch('platform.system', mock.MagicMock(return_value='Darwin'))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemIsDarwin(self):
      print dotfilesinstaller.identifySystem()

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.TextTestRunner().run(suite)
