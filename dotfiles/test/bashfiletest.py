#!/usr/bin/python

import sys
sys.path.insert(0, '../')
import unittest
import io

from dotfiles import bashfile
from systems import Systems

class MockFile(io.StringIO):
  name = None
  def __init__(self, name, buffer_ = None):
    super(MockFile, self).__init__(buffer_)
    self.name = name

class BashfileTest(unittest.TestCase):

  def testBashFileStartsWithShebangAndCorrectHeader(self):
    with io.StringIO() as fileBuffer:
      bashfile.writeHeader(Systems.DARWIN.value, fileBuffer)
      assert(fileBuffer.getvalue().startswith('#!/bin/bash'))
      assert(fileBuffer.getvalue().index('bash_profile') > -1)

suite = unittest.TestLoader().loadTestsFromTestCase(BashfileTest)
unittest.main(module=__name__, buffer=True, exit=False)
