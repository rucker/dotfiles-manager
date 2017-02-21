#!/usr/bin/env python3

import sys
import os
from os.path import join
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotfilesmanager import env
from dotfilesmanager.test import testenv
from dotfilesmanager import dfm
from dotfilesmanager import bashfile
from dotfilesmanager.constants import SYSTEMS, SRCFILES, DOTFILES

class DotfilesManagerIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        env = testenv
        dfm._set_args()
        testenv.setUp()

    @classmethod
    def tearDownClass(self):
        testenv.tearDown()

    def testWhenInputDirIsSetInConfigFileThenItIsStoredInEnv(self):
        testConfigFile = join(testenv.TMP, 'test-config')
        with open(testConfigFile, 'w') as testConfig:
            testConfig.write('input_dir=nowhere')
        oldConfigFile = env.CONFIG_FILE
        dfm.env = env
        env.CONFIG_FILE = testConfigFile
        dfm._set_args()

        dfm._set_env()
        self.assertTrue(env.INPUT_DIR == 'nowhere')

        testenv.CONFIG_FILE = oldConfigFile
        os.remove(testConfigFile)
        env.CONFIG_FILE = oldConfigFile
        dfm.env = testenv

if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
