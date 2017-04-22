import os
from os.path import join
import shutil
import tempfile
import argparse

from dotfilesmanager.test import testfilemocks

TMP_DIR = join(tempfile.gettempdir(), 'dfm')
INPUT_DIR = join(TMP_DIR, 'testsrc/')
OUTPUT_DIR = join(TMP_DIR, 'testoutputfiles/')
BACKUPS_DIR = join(TMP_DIR, 'testbackups/')
IS_GNU = False
parser = argparse.ArgumentParser()
ARGS = ''

def setUp():
    setUpDirs()
    testfilemocks.createInputFiles()

def setUpDirs():
    for dir in [TMP_DIR, INPUT_DIR, OUTPUT_DIR, BACKUPS_DIR]:
        if not os.path.exists(dir):
            os.mkdir(dir)

def clearArgs():
    ARGS = parser.parse_args([])

def tearDown():
    shutil.rmtree(TMP_DIR)
