#!/usr/bin/python

import unittest
import mock
import dotfiles
import platform
import sys
import os
import io
import time

class DotfilesTest(unittest.TestCase):

  def setUp(self):
    dotfiles.init()
    dotfiles.identifySystem()
    dotfiles.cleanUp()
    self.symlinkTarget = 'bar'
    self.macBashOutputFile = dotfiles.macBashOutputFile
    self.macBashOutputDotFile = '.' + self.macBashOutputFile
    self.linuxBashOutputFile = dotfiles.linuxBashOutputFile
    self.linuxBashOutputDotFile = '.' + self.linuxBashOutputFile

  def tearDown(self):
    self.createdSymlink = dotfiles.homeDir + 'foo'
    if os.path.islink(self.createdSymlink):
      os.remove(self.createdSymlink)
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

  def testBashInputFileContentsAreWrittenToOutputFile(self):
    self.inputFileMock = io.StringIO(u'some_token=some_value\n')
    dotfiles.addInputFileContents(self.inputFileMock, False)
    mock = self.inputFileMock.getvalue()
    with open(self.macBashOutputFile,'r') as bashrc:
      result = bashrc.read()
    self.assertTrue(result in mock)

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

  def testBashOutputFileDoesNotContainBashPrivateTokens(self):
    dummyFile = False
    dummyLine = False
    # Set up bash_private file if it doesn't exist or is empty
    # FIXME: This should be done with mocking.
    if not os.path.isfile('bash_private'):
      with open('bash_private','w') as bashPrivate:
        bashPrivate.write('foo=bar')
        dummyFile = True
    elif os.path.getsize('bash_private') == 0:
      with open('bash_private','w') as bashPrivate:
        bashPrivate.write('foo=bar')
        dummyLine = True
    dotfiles.install()
    with open('bash_private','r') as bashPrivate:
      with open(self.macBashOutputFile,'r') as bashrc:
        for line in bashPrivate:
          if line.strip():
            assert(line not in bashrc.read())
    # Clean up bash_private if we created/modified it for this test
    if dummyFile:
      os.remove('bash_private')
    elif dummyLine:
      with open('bash_private', 'w') as bashPrivate:
        bashPrivate.seek(0)
        bashPrivate.truncate()

  def testAllOutputFilesExistAfterInstallation(self):
    dotfiles.main()
    for file in [self.macBashOutputFile, self.macBashOutputDotFile, self.linuxBashOutputFile, self.linuxBashOutputDotFile]:
      if not os.path.isfile(file):
	self.fail("Did not find expected output file: "  + file)

  def testLinuxTokensNotInMacBashOutputFile(self):
    dotfiles.main()
    with open(self.macBashOutputFile,'r') as macBashOutput:
      with open('bash_linux','r') as bashLinux:
        linuxContents = bashLinux.read()
        macContents = macBashOutput.read()
        assert(linuxContents not in macContents)

suite = unittest.TestLoader().loadTestsFromTestCase(DotfilesTest)
unittest.main(module=__name__, buffer=True, exit=False)
