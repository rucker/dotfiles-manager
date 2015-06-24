#!/usr/bin/python

import unittest
import mock
import dotfilesinstaller
import platform
import sys
import os
import io
import time

class DotfilesTest(unittest.TestCase):

  def setUp(self):
    dotfilesinstaller.init()
    dotfilesinstaller.identifySystem()
    dotfilesinstaller.cleanUp()
    self.symlinkTarget = 'bar'
    self.macBashOutputFile = dotfilesinstaller.bashOutputFile
    self.macBashOutputDotFile = '.' + self.macBashOutputFile

  def tearDown(self):
    self.createdSymlink = dotfilesinstaller.homeDir + 'foo'
    if os.path.islink(self.createdSymlink):
      os.remove(self.createdSymlink)
    if os.path.isfile(self.symlinkTarget):
      os.remove(self.symlinkTarget)
    dotfilesinstaller.cleanUp()

  @mock.patch('platform.system', mock.MagicMock(return_value='Darwin'))
  def testWhenSystemIsDarwinInstallerIdentifiesSystemAsDarwin(self):
    dotfilesinstaller.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith('Darwin'))

  @mock.patch('platform.system', mock.MagicMock(return_value='Linux'))
  def testWhenSystemIsLinuxInstallerIdentifiesSystemAsLinux(self):
    dotfilesinstaller.identifySystem()
    assert(sys.stdout.getvalue().strip().endswith('Linux'))

  @mock.patch('platform.system', mock.MagicMock(return_value='Windows'))
  def testWhenSystemIsWindowsInstallerIdentifiesSystemAsWindowsAndExitsWithCode1(self):
    with self.assertRaises(SystemExit) as cm:
      dotfilesinstaller.identifySystem()
      assert(sys.stdout.getvalue().strip().endswith('not supported!'))
      assertEqual(cm.exception.code, 1)

  def testInstallerWillDeleteExistingOutputFiles(self):
    dotfilesinstaller.init()
    dotfilesinstaller.identifySystem()
    self.macBashOutputFile = dotfilesinstaller.bashOutputFile
    with open(self.macBashOutputFile,'a') as bashrc:
      bashrc.write('Test file...')
    with open(self.macBashOutputDotFile,'a') as bashrc:
      bashrc.write('Test file...')
    dotfilesinstaller.cleanUp()
    assert("Removing " + self.macBashOutputFile in sys.stdout.getvalue().strip())
    self.assertFalse(os.path.isfile(self.macBashOutputFile))
    assert("Removing " + self.macBashOutputDotFile in sys.stdout.getvalue().strip())
    self.assertFalse(os.path.isfile(self.macBashOutputDotFile))

  def testWhenOutputFilesDoNotExistInstallerWillNotAttemptDeletion(self):
    if os.path.isfile(self.macBashOutputFile):
      os.remove(self.macBashOutputFile)
    try:
      dotfilesinstaller.cleanUp()
    except OSError, e:
      if e.errno == 2:
        self.fail("Tried to delete nonexistent file!")

  def testBashrcFileStartsWithShebang(self):
    dotfilesinstaller.addBashrcFileHeader()
    with open(self.macBashOutputFile,'r') as bashrc:
      self.assertEquals(bashrc.readline(), "#!/bin/bash\n")

  def testBashInputFileContentsAreWrittenToOutputFile(self):
    self.inputFileMock = io.StringIO(u'some_token=some_value\n')
    dotfilesinstaller.addInputFileContents(self.inputFileMock, False, False)
    foundExpectedResult = False
    mock = self.inputFileMock.getvalue()
    with open(self.macBashOutputFile,'r') as bashrc:
      result = bashrc.read()
    self.assertTrue(result in mock)

  def setUpSymlink(self):
    with open(self.symlinkTarget,'a') as bar:
      dotfilesinstaller.createSymlink(self.symlinkTarget, 'foo')
    self.createdSymlink = dotfilesinstaller.homeDir + 'foo'

  def testWhenSymlinkDoesNotExistItGetsCreated(self):
    self.setUpSymlink()
    try:
      os.stat(self.createdSymlink)
    except OSError:
      self.fail("Symlink " + self.createdSymlink + " not created!")

  def testWhenSymlinkExistsButIsBrokenItGetsDeletedAndReCreated(self):
    dotfilesinstaller.createSymlink(self.symlinkTarget, 'foo')
    dotfilesinstaller.createSymlink(self.macBashOutputFile, 'foo')
    assert("Link is broken." in sys.stdout.getvalue().strip())
    assert("Link created." in sys.stdout.getvalue().strip())

  def testWhenSymlinkExistsAndIsValidItDoesNotGetDeleted(self):
    self.setUpSymlink()
    dotfilesinstaller.createSymlink('bar', 'foo')
    assert("Link is valid." in sys.stdout.getvalue().strip())

  def testBashrcDoesNotContainBashPrivateTokens(self):
    with open('bash_private','r') as bashPrivate:
      dotfilesinstaller.install()
      with open(self.macBashOutputFile,'r') as bashrc:
        assert(bashPrivate.read() not in bashrc.read())

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
