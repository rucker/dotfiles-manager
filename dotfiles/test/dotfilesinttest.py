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

class DotFilesIntTest(unittest.TestCase):

  def setUp(self):
    dotfiles.init()
    env.inputFilesDir = ''
    env.outputFilesDir = ''
    env.homeDir = ''
    testfilemocks.createInputFiles()

  def tearDown(self):
    testfilemocks.destroyInputAndOutputFiles()

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
  def testBashrcNotCreatedInHomeDirOnDarwinSystem(self):
    dotfiles.identifySystem()
    bashfile.compileBashFiles()
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASHRC.value))

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
  def testBashProfileNotCreatedInHomeDirOnLinuxSystem(self):
    dotfiles.identifySystem()
    bashfile.compileBashFiles()
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASH_PROFILE.value))

  def testValidSymlinkToVimrcIsCreated(self):
    bashfile.compileBashFiles()
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertTrue(os.path.isfile(VimFiles.DOT_VIMRC.value))

  def testWhenSymlinkDoesNotExistItGetsCreated(self):
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    try:
      os.stat(VimFiles.DOT_VIMRC.value)
      self.assertTrue("Link created." in sys.stdout.getvalue().strip())
    except OSError:
      self.fail("Symlink " + VimFiles.DOT_VIMRC.value + " not created!")

  def testWhenSymlinkExistsItGetsReported(self):
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertTrue("Link already exists." in sys.stdout.getvalue().strip())

  def testWhenDotFileExistsInHomeDirAndIsRegularFileItGetsRenamedAndANewSymlinkIsCreated(self):
    with open(VimFiles.DOT_VIMRC.value, 'w') as vimrc:
      vimrc.write("foo bar baz")
    bashfile.compileBashFiles()
    dotfiles.symlink(VimFiles.VIMRC.value, VimFiles.DOT_VIMRC.value)
    self.assertTrue("Renaming" in sys.stdout.getvalue().strip())
    self.assertTrue("Link created." in sys.stdout.getvalue().strip())
    os.remove(VimFiles.DOT_VIMRC.value + '.bak')

suite = unittest.TestLoader().loadTestsFromTestCase(DotFilesIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
