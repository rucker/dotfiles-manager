#!/usr/bin/env python3

import sys
import os
import unittest
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager import bashfile
from dotfilesmanager.constants import BASHFILES

class BashFileTest(unittest.TestCase):

    def testBashFileStartsWithShebangAndCorrectHeader(self):
        with io.StringIO() as fileBuffer:
            bashfile._write_header(BASHFILES.BASH_PROFILE.value, fileBuffer)
            self.assertTrue(fileBuffer.getvalue().startswith('#!/bin/bash'))
            self.assertTrue(fileBuffer.getvalue().index(BASHFILES.BASH_PROFILE.value) > -1)

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
