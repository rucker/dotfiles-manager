#!/usr/bin/python

import unittest
import mock
import dotfiles
import platform
import sys
import os
import io
import time

class MockFile(io.StringIO):
  name = None
  def __init__(self, name, buffer_ = None):
    super(MockFile, self).__init__(buffer_)
    self.name = name

class DotfilesTest(unittest.TestCase):

  def setUp(self):
    dotfiles.init()
    dotfiles.identifySystem()
    dotfiles.cleanUp()
    self.symlinkTarget = 'bar'
    self.regularFile = dotfiles.homeDir + 'foo'
    self.macBashOutputFile = dotfiles.macBashOutputFile
    self.macBashOutputDotFile = '.' + self.macBashOutputFile
    self.linuxBashOutputFile = dotfiles.linuxBashOutputFile
    self.linuxBashOutputDotFile = '.' + self.linuxBashOutputFile
    self.inputFilesDir = '../inputfiles/'
    self.bashLinux = self.inputFilesDir + 'bash_linux'
    self.bashPrivate = self.inputFilesDir + 'bash_private'

  def tearDown(self):
    self.createdSymlink = dotfiles.homeDir + 'foo'
    if os.path.islink(self.createdSymlink):
      os.remove(self.createdSymlink)
    if os.path.isfile(self.regularFile):
      os.remove(self.regularFile)
    if os.path.isfile(self.regularFile + '.bak'):
      os.remove(self.regularFile + '.bak')
    if os.path.isfile(self.symlinkTarget):
      os.remove(self.symlinkTarget)
    dotfiles.cleanUp()

  @mock.patch('platform.system', mock.MagicMock(return_value='Darwin'))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
    dotfiles.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith('Darwin'))

  @mock.patch('platform.system', mock.MagicMock(return_value='Linux'))
  def testWhenSystemIsLinuxInstallerIdentifiesSystemAsLinux(self):
    dotfiles.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith('Linux'))

  @mock.patch('platform.system', mock.MagicMock(return_value='Windows'))
  def testWhenSystemIsWindowsInstallerIdentifiesSystemAsWindowsAndExitsWithCode1(self):
    with self.assertRaises(SystemExit) as cm:
      dotfiles.identifySystem()
      assert(sys.stdout.getvalue().strip().endswith('not supported!'))
      assertEqual(cm.exception.code, 1)

  def testInstallerWillDeleteExistingOutputFiles(self):
    dotfiles.init()
    dotfiles.identifySystem()
    self.macBashOutputFile = dotfiles.macBashOutputFile
    for file in [self.macBashOutputFile, self.macBashOutputDotFile, self.linuxBashOutputFile, self.linuxBashOutputDotFile]:
      with open(file,'a') as bash:
        bash.write('Test file...')
    dotfiles.cleanUp()

    for file in [self.macBashOutputFile, self.macBashOutputDotFile, self.linuxBashOutputFile, self.linuxBashOutputDotFile]:
      assert("Removing " + file in sys.stdout.getvalue().strip())
      self.assertFalse(os.path.isfile(file))

  def testWhenOutputFilesDoNotExistInstallerWillNotAttemptDeletion(self):
    if os.path.isfile(self.macBashOutputFile):
      os.remove(self.macBashOutputFile)
    try:
      dotfiles.cleanUp()
    except OSError, e:
      if e.errno == 2:
        self.fail("Tried to delete nonexistent file!")

  def testBashOutputFileStartsWithShebang(self):
    dotfiles.addBashOutputFileHeader()
    with open(self.macBashOutputFile,'r') as bashrc:
      self.assertEquals(bashrc.readline(), "#!/bin/bash\n")

  def testBashLinuxFileContentsAreWrittenToOutputFile(self):
    self.bashLinuxFileMock = MockFile(self.bashLinux, u'some_token=some_value\n')
    dotfiles.addInputFileContents(self.bashLinuxFileMock, False)
    with open(self.linuxBashOutputFile,'r') as bashrc:
      self.assertTrue(bashrc.read() in self.bashLinuxFileMock.getvalue())

  def testBashOutputFileDoesNotContainBashPrivateTokens(self):
    self.bashLinuxFileMock = MockFile(self.bashLinux, u'some_token=some_value\n')
    self.bashPrivateFileMock = MockFile(self.bashPrivate, u'private_token=private_value\n')
    dotfiles.addInputFileContents(self.bashLinuxFileMock, False)
    dotfiles.addInputFileContents(self.bashPrivateFileMock, False)
    with open(self.linuxBashOutputFile,'r') as bashrc:
      self.assertTrue(bashrc.read() not in self.bashPrivateFileMock.getvalue())

  def setUpSymlink(self):
    with open(self.symlinkTarget,'a') as bar:
      dotfiles.createSymlink(self.symlinkTarget, 'foo')
    self.createdSymlink = dotfiles.homeDir + 'foo'

  def testWhenSymlinkDoesNotExistItGetsCreated(self):
    self.setUpSymlink()
    try:
      os.stat(self.createdSymlink)
    except OSError:
      self.fail("Symlink " + self.createdSymlink + " not created!")

  def testWhenSymlinkExistsButIsBrokenItGetsDeletedAndReCreated(self):
    dotfiles.createSymlink(self.symlinkTarget, 'foo')
    dotfiles.createSymlink(self.macBashOutputFile, 'foo')
    assert("Link is broken." in sys.stdout.getvalue().strip())
    assert("Link created." in sys.stdout.getvalue().strip())

  def testWhenSymlinkExistsAndIsValidItDoesNotGetDeleted(self):
    self.setUpSymlink()
    dotfiles.createSymlink('bar', 'foo')
    assert("Link is valid." in sys.stdout.getvalue().strip())

  def testWhenSymlinkSourceExistsAndIsRegularFileItGetsRenamed(self):
    with open(self.regularFile,'w') as source:
      source.write('some_token=some_value')
    self.setUpSymlink()
    dotfiles.createSymlink('bar','foo')
    assert("Renaming" in sys.stdout.getvalue().strip())
    self.assertFalse(os.path.isfile(self.regularFile))
    self.assertTrue(os.path.isfile(self.regularFile + '.bak'))

  def testLinuxTokensNotInMacBashOutputFile(self):
    dotfiles.main()
    with open(self.macBashOutputFile,'r') as macBashOutput:
      with open(self.bashLinux,'r') as bashLinux:
        linuxContents = bashLinux.read()
        macContents = macBashOutput.read()
        assert(linuxContents not in macContents)

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
