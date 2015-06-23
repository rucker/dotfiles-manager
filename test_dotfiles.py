#!/usr/bin/python

import unittest
import mock
import dotfilesinstaller
import platform
import sys

class DotfilesTest(unittest.TestCase):
  @mock.patch('platform.system', mock.MagicMock(return_value='Darwin'))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
    dotfilesinstaller.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith('Darwin'))

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
