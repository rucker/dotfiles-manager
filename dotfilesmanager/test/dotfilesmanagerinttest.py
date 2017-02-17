#!/usr/bin/env python

import sys
import os
from os.path import join
import unittest

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dfm
import bashfile
from constants import SYSTEMS, SRCFILES, DOTFILES

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

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesManagerIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
