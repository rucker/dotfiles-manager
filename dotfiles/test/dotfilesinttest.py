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
    testfilemocks.createInputFiles()

  @classmethod
  def tearDownClass(self):
    testfilemocks.destroyInputAndOutputFiles()

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
  def testBashrcNotCreatedInHomeDirOnDarwinSystem(self):
    bashfile.compileBashFiles()
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASHRC.value))

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
  def testBashProfileNotCreatedInHomeDirOnLinuxSystem(self):
    bashfile.compileBashFiles()
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASH_PROFILE.value))

  def testValidSymlinkToVimrcIsCreated(self):
    bashfile.compileBashFiles()
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertTrue(os.path.isfile(VimFiles.DOT_VIMRC.value))

  def testWhenDotVimrcExistsInHomeDirAndIsRegularFileItGetsDeleted(self):
    os.remove(VimFiles.DOT_VIMRC.value)
    with open(VimFiles.DOT_VIMRC.value, 'w') as vimrc:
      vimrc.write("foo bar baz")
    bashfile.compileBashFiles()
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertTrue("Deleted." in sys.stdout.getvalue().strip())

suite = unittest.TestLoader().loadTestsFromTestCase(BashFileIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
