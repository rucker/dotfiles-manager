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
from constants import Systems, Srcfiles, Dotfiles

class DotfilesIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dotfilesmanager.env = testenv
        dotfilesmanager.ioutils.env = testenv
        dotfilesmanager.bashfile.env = testenv
        dotfilesmanager.setArgs()
        testenv.setUp()

    @classmethod
    def tearDownClass(self):
        testenv.tearDown()

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
    def testBashrcNotCreatedInHomeDirOnDarwinSystem(self):
        dotfilesmanager.identifySystem()
        bashfile.compileBashFiles()
        self.assertFalse(os.path.isfile(Dotfiles.BASHRC.value))

    @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
    def testBashProfileNotCreatedInHomeDirOnLinuxSystem(self):
        dotfilesmanager.identifySystem()
        bashfile.compileBashFiles()
        self.assertFalse(os.path.isfile(Dotfiles.BASH_PROFILE.value))

    def testWhenInputDirIsSetInConfigFileThenItIsStoredInEnv(self):
        testConfigFile = testenv.tmp + 'test-config'
        with open(testConfigFile, 'w') as testConfig:
            testConfig.write('inputDir=nowhere')
        oldConfigFile = env.configFile
        dotfilesmanager.env = env
        env.configFile = testConfigFile
        dotfilesmanager.setArgs()

        dotfilesmanager.setEnv()
        self.assertTrue(env.inputDir == 'nowhere/')

        testenv.configFile = oldConfigFile
        os.remove(testConfigFile)
        env.configFile = oldConfigFile
        dotfilesmanager.env = testenv

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
