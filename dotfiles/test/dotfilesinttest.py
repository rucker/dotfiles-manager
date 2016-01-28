#!/usr/bin/python

import sys
import os
import shutil
import unittest
import mock

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
    env.homeBinDir = 'some-fake-dir/'

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
    self.createVimrcSymlink()
    try:
      os.stat(env.homeDir + VimFiles.DOT_VIMRC.value)
      self.assertTrue("Link created." in sys.stdout.getvalue().strip())
    except OSError as e:
      print e
      self.fail("Symlink " + env.homeDir + VimFiles.DOT_VIMRC.value + " not created!")

  def testWhenSymlinkExistsItGetsReported(self):
    self.createVimrcSymlink()
    self.createVimrcSymlink()
    self.assertTrue("Link already exists." in sys.stdout.getvalue().strip())

  def testWhenDotFileExistsInHomeDirAndIsRegularFileItGetsRenamedAndANewSymlinkIsCreated(self):
     with open(env.homeDir + VimFiles.DOT_VIMRC.value, 'w') as vimrc:
       vimrc.write("foo bar baz")
     bashfile.compileBashFiles()
     self.createVimrcSymlink()
     self.assertTrue("Renaming" in sys.stdout.getvalue().strip())
     self.assertTrue("Link created." in sys.stdout.getvalue().strip())
     os.remove(env.homeDir + VimFiles.DOT_VIMRC.value + '.bak')

  def testWhenHomeBinDirDoesNotExistUserIsAskedIfItShouldBeCreated(self):
    with mock.patch('__builtin__.raw_input', return_value='n'):
      dotfiles.createSymlinks()
      self.assertTrue(env.homeBinDir + " does not exist" in sys.stdout.getvalue().strip())
      self.assertFalse(os.path.exists(env.homeBinDir))

  def testWhenHomeBinDirDoesNotExistUserIsAskedIfItShouldBeCreated(self):
    with mock.patch('__builtin__.raw_input', return_value='y'):
      dotfiles.createSymlinks()
      self.assertTrue(env.homeBinDir + " does not exist" in sys.stdout.getvalue().strip())
      self.assertTrue(os.path.exists(env.homeBinDir))
      shutil.rmtree(env.homeBinDir)

  def testWhenDotFileExistsInHomeDirAndIsRegularFileUserCanChooseToKeepThatFile(self):
    with open(env.homeDir + VimFiles.DOT_VIMRC.value, 'w') as vimrc:
      vimrc.write("foo bar baz")
    with mock.patch('__builtin__.raw_input', return_value='n'):
      bashfile.compileBashFiles()
      self.createVimrcSymlink()
      dotfiles.cleanUp()
      bakFile = env.homeDir + VimFiles.DOT_VIMRC.value + '.bak'
      self.assertTrue("Link created." in sys.stdout.getvalue().strip())
      self.assertTrue("The existing file " + env.homeDir + VimFiles.DOT_VIMRC.value + " was renamed to " + bakFile in sys.stdout.getvalue().strip())
      self.assertTrue("Keeping file " + bakFile in sys.stdout.getvalue().strip())
      self.assertTrue(os.path.isfile(bakFile))
      os.remove(bakFile)

  def testWhenDotFileExistsInHomeDirAndIsRegularFileUserCanChooseToDeleteThatFile(self):
    with open(env.homeDir + VimFiles.DOT_VIMRC.value, 'w') as vimrc:
      vimrc.write("foo bar baz")
    with mock.patch('__builtin__.raw_input', return_value='y'):
      bashfile.compileBashFiles()
      self.createVimrcSymlink()
      dotfiles.cleanUp()
      bakFile = env.homeDir + VimFiles.DOT_VIMRC.value + '.bak'
      self.assertTrue("Link created." in sys.stdout.getvalue().strip())
      self.assertTrue("The existing file " + env.homeDir + VimFiles.DOT_VIMRC.value + " was renamed to " + bakFile in sys.stdout.getvalue().strip())
      self.assertTrue("Deleting file " + bakFile in sys.stdout.getvalue().strip())
      self.assertFalse(os.path.isfile(bakFile))

  def createVimrcSymlink(self):
    dotfiles.symlink(env.outputFilesDir + VimFiles.VIMRC.value, env.homeDir + VimFiles.DOT_VIMRC.value)

suite = unittest.TestLoader().loadTestsFromTestCase(DotFilesIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
