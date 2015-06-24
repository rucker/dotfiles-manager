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
  symlinkTarget = 'bar'
  createdSymlink = ''
  bashrcFile = 'bashrc'
  inputFileMock = io.StringIO(u'some_token=some_value\n')

  def setUp(self):
    dotfilesinstaller.init()
    dotfilesinstaller.cleanUp()

  def tearDown(self):
    self.createdSymlink = dotfilesinstaller.homeDir + 'foo'
    if os.path.islink(self.createdSymlink):
      os.remove(self.createdSymlink)
    if os.path.isfile(self.symlinkTarget):
      os.remove(self.symlinkTarget)
    if os.path.isfile(self.bashrcFile):
      os.remove(self.bashrcFile)

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

  def testWhenBashrcExistsInstallerWillDeleteIt(self):
    if not os.path.isfile(self.bashrcFile):
      testbashrc = open(self.bashrcFile,'w')
      testbashrc.write('Test file...')
      testbashrc.close()
    dotfilesinstaller.cleanUp()
    assert(sys.stdout.getvalue().strip().endswith(self.bashrcFile))
    self.assertFalse(os.path.isfile(self.bashrcFile))

  def testWhenBashrcDoesNotExistInstallerWillNotAttemptDeletion(self):
    if os.path.isfile(self.bashrcFile):
      os.remove(self.bashrcFile)
    try:
      dotfilesinstaller.cleanUp()
    except OSError:
      self.fail("Tried to delete nonexistent file!")

  def testBashrcFileStartsWithShebang(self):
    dotfilesinstaller.writeFileHeader()
    with open(self.bashrcFile,'r') as bashrc:
      self.assertEquals(bashrc.readline(), "#!/bin/bash\n")

  def testBashInputFileContentsAreWrittenToBashrc(self):
    dotfilesinstaller.writeSection(self.inputFileMock, False)
    foundExpectedResult = False
    mock = self.inputFileMock.getvalue()
    with open(self.bashrcFile,'r') as bashrc:
      result = bashrc.read()
    self.assertTrue(result in mock)

  def setUpSymlink(self):
    global createdSymlink
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
    dotfilesinstaller.createSymlink(self.bashrcFile, 'foo')
    assert("Link is broken." in sys.stdout.getvalue().strip())
    assert("Link created." in sys.stdout.getvalue().strip())

  def testWhenSymlinkExistsAndIsValidItDoesNotGetDeleted(self):
    self.setUpSymlink()
    dotfilesinstaller.createSymlink('bar', 'foo')
    assert("Link is valid." in sys.stdout.getvalue().strip())

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
