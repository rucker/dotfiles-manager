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
        testenv.clearArgs()
        testenv.tearDown()

    def testWhenVimrcIsWrittenAndUserPassesArg_no_local_ItContainsTheContentsOfVimrcButNotVimrcLocal(self):
        env.args = env.parser.parse_args(['--no-local'])
        vimrc.compileVimrc()
        with open(env.outputDir + Dotfiles.VIMRC.value) as dotVimrc:
            with open(env.srcDir + Srcfiles.VIMRC.value) as vimrcFile:
                with open(env.srcDir + Srcfiles.VIMRC_LOCAL.value) as vimrcLocal:
                    contents = dotVimrc.read()
                    self.assertTrue(vimrcFile.read() in contents)
                    self.assertTrue(vimrcLocal.read() not in contents)

    def testWhenVimrcIsWrittenAndUserDoesNotPassArg_no_local_ItContainsTheContentsOfVimrcAndVimrcLocal(self):
        vimrc.compileVimrc()
        with open(env.outputDir + Dotfiles.VIMRC.value) as dotVimrc:
            with open(env.srcDir + Srcfiles.VIMRC.value) as vimrcFile:
                with open(env.srcDir + Srcfiles.VIMRC_LOCAL.value) as vimrcLocal:
                    contents = dotVimrc.read()
                    self.assertTrue(vimrcFile.read() in contents)
                    self.assertTrue(vimrcLocal.read() in contents)

suite = unittest.TestLoader().loadTestsFromTestCase(VimrcIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
