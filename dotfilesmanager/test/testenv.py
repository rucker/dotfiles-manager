import os
from os.path import join
import shutil
import tempfile
import argparse

import testfilemocks
from constants import MISC
import ioutils
from ioutils import eprint

TMP = join(tempfile.gettempdir(), 'dfm')
INPUT_DIR = join(TMP, 'testsrc/')
OUTPUT_DIR = join(TMP, 'testoutputfiles/')
BACKUPS_DIR = join(TMP, 'testbackups/')
CONFIG_FILE = join(TMP, MISC.CONFIG_FILE.value)
parser = argparse.ArgumentParser()
ARGS = ''

def setUp():
    setUpDirs()
    testfilemocks.createInputFiles()

def setUpDirs():
    for dir in [TMP, INPUT_DIR, OUTPUT_DIR, BACKUPS_DIR]:
        if not os.path.exists(dir):
            os.mkdir(dir)
    ioutils.create_file(CONFIG_FILE, 'input_dir=' + INPUT_DIR)

def clearArgs():
    ARGS = parser.parse_args([])

def tearDown():
    shutil.rmtree(TMP)
