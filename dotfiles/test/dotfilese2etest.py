#!/usr/bin/python

import sys
import os
import unittest
import mock

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import dotfiles
import testfilemocks
from dotfiles import bashfile
from constants import Systems, BashInputFiles, BashOutputFiles, VimFiles

class BashFileIntTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    dotfiles.init()
    env.inputFilesDir = ''
    env.outputFilesDir = ''
    env.homeDir = ''
    testfilemocks.createInputFiles()

  @classmethod
  def tearDownClass(self):
    testfilemocks.destroyInputAndOutputFiles()

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
  def testBashrcNotCreatedInHomeDirOnDarwinSystem(self):
    dotfiles.main()
    self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASHRC.value))

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
  def testBashProfileNotCreatedInHomeDirOnLinuxSystem(self):
    dotfiles.main()
    self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASH_PROFILE.value))

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
