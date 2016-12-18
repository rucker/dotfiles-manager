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
import gitconfig
from constants import GitConfigInputFiles, GitConfigOutputFiles

class GitConfigIntTest(unittest.TestCase):

    def setUp(self):
        dotfilesmanager.init()
        testenv.setUp()

    def tearDown(self):
        testenv.tearDown()

    def testWhenGitConfigFileIsWrittenItContainsTheContentsOfGitPublicButNotGitPrivate(self):
        gitconfig.compileGitConfig()
        with open(env.outputFilesDir + GitConfigOutputFiles.GITCONFIG.value) as dotGitConfig:
            with open(env.inputFilesDir + GitConfigInputFiles.GIT_PUBLIC.value) as gitPublic:
                with open(env.inputFilesDir + GitConfigInputFiles.GIT_PRIVATE.value) as gitPrivate:
                    contents = dotGitConfig.read()
                    self.assertTrue(gitPublic.read() in contents)
                    self.assertTrue(gitPrivate.read() not in contents)

    def testWhenGitConfigDotFileIsWrittenItContainsTheContentsOfGitPublicAndGitPrivate(self):
        gitconfig.compileGitConfig()
        with open(env.homeDir + GitConfigOutputFiles.DOT_GITCONFIG.value) as dotGitConfig:
            with open(env.inputFilesDir + GitConfigInputFiles.GIT_PUBLIC.value) as gitPublic:
                with open(env.inputFilesDir + GitConfigInputFiles.GIT_PRIVATE.value) as gitPrivate:
                    contents = dotGitConfig.read()
                    self.assertTrue(gitPublic.read() in contents)
                    self.assertTrue(gitPrivate.read() in contents)

suite = unittest.TestLoader().loadTestsFromTestCase(GitConfigIntTest)
unittest.main(module=__name__, buffer=True, exit=False)
