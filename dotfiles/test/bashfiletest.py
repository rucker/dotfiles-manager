#!/usr/bin/python

import sys
import unittest
import io
import __builtin__

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import bashfile
from constants import Systems, BashOutputFiles

class BashFileTest(unittest.TestCase):

  def testBashFileStartsWithShebangAndCorrectHeader(self):
    buffer = bashfile.createHeadBuffer(BashOutputFiles.BASH_PROFILE.value)
    self.assertTrue(buffer.getvalue().startswith('#!/bin/bash'))
    self.assertTrue(buffer.getvalue().index(BashOutputFiles.BASH_PROFILE.value) > -1)

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileTest)
unittest.main(module=__name__, buffer=True, exit=False)
