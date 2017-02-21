#!/usr/bin/env python3

import sys
import os
import unittest
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager import bashfile
from dotfilesmanager.constants import SYSTEMS, DOTFILES

class BashFileTest(unittest.TestCase):

    def testBashFileStartsWithShebangAndCorrectHeader(self):
        with io.StringIO() as fileBuffer:
            bashfile._write_header(DOTFILES.BASH_PROFILE.value, fileBuffer)
            self.assertTrue(fileBuffer.getvalue().startswith('#!/bin/bash'))
            self.assertTrue(fileBuffer.getvalue().index(DOTFILES.BASH_PROFILE.value) > -1)

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
