#!/usr/bin/python

import sys
import os
import unittest
import mock

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dotfilesmanager
import ioutils
import testfilemocks
from constants import Systems, BashInputFiles, BashOutputFiles, VimFiles, GitConfigOutputFiles

class IOUtilsIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dotfilesmanager.init()
        testenv.setUp()

    @classmethod
    def tearDownClass(self):
        testenv.tearDown()

    def testWhenUserPassesArg_r_AndEnters_Y_whenPromptedThenDotfilesAreRestoredToMostRecentBackedUpVersion(self):
        with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value, 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_alternate_value")
        with open(env.backupsDir + BashOutputFiles.BASH_PROFILE.value + '_2016-07-07_14-40-00.bak', 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_alternate_value")
        with open(env.backupsDir + BashOutputFiles.BASH_PROFILE.value + '_2016-07-07_14-43-00.bak', 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_newer_alternate_value")
        with mock.patch('__builtin__.raw_input', return_value='y'):
            ioutils.revertDotFiles([BashOutputFiles.DOT_BASH_PROFILE.value])
        with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value) as bash_profile:
            self.assertTrue("some_newer_alternate_value" in bash_profile.read())

    def testWhenUserPassesArg_r_AndEnters_N_whenPromptedThenBackedUpDotfilesAreNotRestored(self):
        with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value, 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_alternate_value")
        with open(env.backupsDir + BashOutputFiles.DOT_BASH_PROFILE.value + '_2016-07-07_14-40-00.bak', 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_alternate_value")
        with open(env.backupsDir + BashOutputFiles.BASH_PROFILE.value + '_2016-07-07_14-43-00.bak', 'w') as bash_profile:
            bash_profile.write("some_bash_token=some_newer_alternate_value")
        with mock.patch('__builtin__.raw_input', return_value='n'):
            ioutils.revertDotFiles([BashOutputFiles.DOT_BASH_PROFILE.value])
        with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value) as bash_profile:
            self.assertTrue("some_newer_alternate_value" not in bash_profile.read())

suite = unittest.TestLoader().loadTestsFromTestCase(IOUtilsIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
