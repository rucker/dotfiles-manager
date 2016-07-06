#!/usr/bin/python

import sys
import os
import unittest
import mock

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dotfiles
import ioutils
import testfilemocks
from constants import Systems, BashInputFiles, BashOutputFiles, VimFiles, GitConfigOutputFiles

class IOUtilsIntTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    dotfiles.init()
    testenv.setUp()

  @classmethod
  def tearDownClass(self):
    testenv.tearDown()

  def testWhenUserPassesArg_r_AndEnters_Y_whenPromptedThenBackedUpDotfilesAreRestored(self):
    with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value, 'w') as bash_profile:
      bash_profile.write("some_bash_token=some_alternate_value")
    with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value + '.bak', 'w') as bash_profile:
      bash_profile.write("some_bash_token=some_alternate_value")
    with mock.patch('__builtin__.raw_input', return_value='y'):
      ioutils.revertDotFiles([ BashOutputFiles.DOT_BASH_PROFILE.value, BashOutputFiles.DOT_BASHRC.value, VimFiles.DOT_VIMRC.value, GitConfigOutputFiles.DOT_GITCONFIG.value ])
    self.assertTrue("An older version" in sys.stdout.getvalue().strip())
    self.assertFalse(os.path.isfile(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value + '.bak'))
    env.args = ''

  def testWhenUserPassesArg_r_AndEnters_N_whenPromptedThenBackedUpDotfilesAreNotRestored(self):
    with open(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value, 'w') as bash_profile:
      bash_profile.write("some_bash_token=some_alternate_value")
    with open(env.backupsDir + BashOutputFiles.DOT_BASH_PROFILE.value + '.bak', 'w') as bash_profile:
      bash_profile.write("some_bash_token=some_alternate_value")
    with mock.patch('__builtin__.raw_input', return_value='n'):
      ioutils.revertDotFiles([ BashOutputFiles.DOT_BASH_PROFILE.value, BashOutputFiles.DOT_BASHRC.value, VimFiles.DOT_VIMRC.value, GitConfigOutputFiles.DOT_GITCONFIG.value ])
    self.assertTrue("An older version" in sys.stdout.getvalue().strip())
    self.assertTrue(os.path.isfile(env.homeDir + BashOutputFiles.DOT_BASH_PROFILE.value + '.bak'))
    env.args = ''

suite = unittest.TestLoader().loadTestsFromTestCase(IOUtilsIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
