#!/usr/bin/python

import sys
import os
import shutil
import unittest
import mock
import fnmatch
import time

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dotfilesmanager
import bashfile
from constants import Systems, BashInputFiles, BashOutputFiles, VimFiles

class DotFilesIntTest(unittest.TestCase):

    def setUp(self):
        dotfilesmanager.init()
        testenv.setUp()

    def tearDown(self):
        testenv.tearDown()

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
    def testBashrcNotCreatedInHomeDirOnDarwinSystem(self):
        dotfilesmanager.identifySystem()
        bashfile.compileBashFiles()
        self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASHRC.value))

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
    def testBashProfileNotCreatedInHomeDirOnLinuxSystem(self):
        dotfilesmanager.identifySystem()
        bashfile.compileBashFiles()
        self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASH_PROFILE.value))

suite = unittest.TestLoader().loadTestsFromTestCase(DotFilesIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
