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
import dotfiles
import bashfile
from constants import Systems, BashInputFiles, BashOutputFiles, VimFiles

class DotFilesIntTest(unittest.TestCase):

  def setUp(self):
    dotfiles.init()
    testenv.setUp()

  def tearDown(self):
    testenv.tearDown()

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.DARWIN.value))
  def testBashrcNotCreatedInHomeDirOnDarwinSystem(self):
    dotfiles.identifySystem()
    bashfile.compileBashFiles()
    self.createVimrcSymlink()
    self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASHRC.value))

  @mock.patch('platform.system', mock.MagicMock(return_value=Systems.LINUX.value))
  def testBashProfileNotCreatedInHomeDirOnLinuxSystem(self):
    dotfiles.identifySystem()
    bashfile.compileBashFiles()
    self.createVimrcSymlink()
    self.assertFalse(os.path.isfile(BashOutputFiles.DOT_BASH_PROFILE.value))

  def testValidSymlinkToVimrcIsCreated(self):
    bashfile.compileBashFiles()
    self.createVimrcSymlink()
    self.assertTrue(os.path.isfile(env.homeDir + VimFiles.DOT_VIMRC.value))

  def testWhenSymlinkDoesNotExistItGetsCreated(self):
    env.args = env.parser.parse_args(['-v'])
    self.createVimrcSymlink()
    try:
      os.stat(env.homeDir + VimFiles.DOT_VIMRC.value)
      self.assertTrue("Link created." in sys.stdout.getvalue().strip())
    except OSError as e:
      print e
      self.fail("Symlink " + env.homeDir + VimFiles.DOT_VIMRC.value + " not created!")

  def testWhenSymlinkExistsItGetsReported(self):
    env.args = env.parser.parse_args(['-v'])
    self.createVimrcSymlink()
    self.createVimrcSymlink()
    self.assertTrue("Link already exists." in sys.stdout.getvalue().strip())

  def testWhenDotFileExistsInHomeDirAndIsRegularFileItGetsBackedUpAndANewSymlinkIsCreated(self):
    env.args = env.parser.parse_args(['-v'])
    with open(env.homeDir + VimFiles.DOT_VIMRC.value, 'w') as vimrc:
      vimrc.write("foo bar baz")
    bashfile.compileBashFiles()
    self.createVimrcSymlink()
    self.assertTrue("Backing up" in sys.stdout.getvalue().strip())
    self.assertTrue("Link created." in sys.stdout.getvalue().strip())
    backupFound = False
    matchPattern = VimFiles.VIMRC.value + '_' + time.strftime('%Y-%m-%d') + '*.bak'
    for obj in os.walk(env.backupsDir):
      file = obj[2][0]
      if fnmatch.fnmatch(file, matchPattern):
        backupFound = True
    self.assertTrue(backupFound)

  def createVimrcSymlink(self):
    dotfiles.symlink(env.outputFilesDir + VimFiles.VIMRC.value, env.homeDir + VimFiles.DOT_VIMRC.value)

suite = unittest.TestLoader().loadTestsFromTestCase(DotFilesIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
