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
        with io.StringIO() as fileBuffer:
            bashfile.writeHeader(BashOutputFiles.BASH_PROFILE.value, fileBuffer)
            self.assertTrue(fileBuffer.getvalue().startswith('#!/bin/bash'))
            self.assertTrue(fileBuffer.getvalue().index(BashOutputFiles.BASH_PROFILE.value) > -1)

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileTest)
unittest.main(module=__name__, buffer=True, exit=False)
