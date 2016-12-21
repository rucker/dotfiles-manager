#!/usr/bin/python

import sys
import os
import shutil
import unittest
import mock

sys.path.insert(0, sys.path[0][:sys.path[0].rfind('test')])

import env
import testenv
import dotfilesmanager
import testfilemocks
import vimrc
from constants import Srcfiles, Dotfiles

class VimrcIntTest(unittest.TestCase):

    def setUp(self):
        dotfilesmanager.init()
        testenv.setUp()

    def tearDown(self):
        testenv.tearDown()

    def testWhenVimrcFileIsWrittenItContainsTheContentsOfVimrcButNotVimrcLocal(self):
        vimrc.compileVimrc()
        with open(env.outputFilesDir + Dotfiles.VIMRC.value) as dotVimrc:
            with open(env.inputFilesDir + Srcfiles.VIMRC.value) as vimrcFile:
                with open(env.inputFilesDir + Srcfiles.VIMRC_LOCAL.value) as vimrcLocal:
                    contents = dotVimrc.read()
                    self.assertTrue(vimrcFile.read() in contents)
                    self.assertTrue(vimrcLocal.read() not in contents)

    def testWhenVimrcDotFileIsWrittenItContainsTheContentsOfVimrcAndVimrcLocal(self):
        vimrc.compileVimrc()
        with open(env.homeDir + Dotfiles.VIMRC.value) as dotVimrc:
            with open(env.inputFilesDir + Srcfiles.VIMRC.value) as vimrcFile:
                with open(env.inputFilesDir + Srcfiles.VIMRC_LOCAL.value) as vimrcLocal:
                    contents = dotVimrc.read()
                    self.assertTrue(vimrcFile.read() in contents)
                    self.assertTrue(vimrcLocal.read() in contents)

suite = unittest.TestLoader().loadTestsFromTestCase(VimrcIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
