#!/usr/bin/python

import sys
import unittest
import io
import __builtin__
from mock import mock_open, patch

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

from dotfiles import bashfile
from constants import Systems, BashInputFiles

class BashFileTest(unittest.TestCase):

  def testBashFileStartsWithShebangAndCorrectHeader(self):
    with io.StringIO() as fileBuffer:
      bashfile.writeHeader('.bash_profile', fileBuffer)
      self.assertTrue(fileBuffer.getvalue().startswith('#!/bin/bash'))
      self.assertTrue(fileBuffer.getvalue().index('.bash_profile') > -1)

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileTest)
unittest.main(module=__name__, buffer=True, exit=False)
