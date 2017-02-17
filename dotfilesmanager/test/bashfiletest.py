#!/usr/bin/env python

import sys
import unittest
import io

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import bashfile
from constants import SYSTEMS, DOTFILES

class BashFileTest(unittest.TestCase):

    def testBashFileStartsWithShebangAndCorrectHeader(self):
        with io.StringIO() as fileBuffer:
            bashfile._write_header(DOTFILES.BASH_PROFILE.value, fileBuffer)
            self.assertTrue(fileBuffer.getvalue().startswith('#!/bin/bash'))
            self.assertTrue(fileBuffer.getvalue().index(DOTFILES.BASH_PROFILE.value) > -1)

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileTest)
unittest.main(module=__name__, buffer=True, exit=False)
