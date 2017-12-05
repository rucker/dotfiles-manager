import os
from os.path import join
import shutil
import tempfile
import argparse


_TMP_DIR = join(tempfile.gettempdir(), 'dfm')
INPUT_DIR = None
OUTPUT_DIR = None
BACKUPS_DIR = None
parser = None
ARGS = None

def set_up():
    global INPUT_DIR
    global OUTPUT_DIR
    global BACKUPS_DIR
    global parser
    global ARGS
    INPUT_DIR = join(_TMP_DIR, 'testsrc/')
    OUTPUT_DIR = join(_TMP_DIR, 'testoutputfiles/')
    BACKUPS_DIR = join(_TMP_DIR, 'testbackups/')
    parser = argparse.ArgumentParser()
    ARGS = None
    _set_up_dirs()

def _set_up_dirs():
    for tmp_dir in [_TMP_DIR, INPUT_DIR, OUTPUT_DIR, BACKUPS_DIR]:
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)

def tear_down():
    shutil.rmtree(_TMP_DIR)
    global INPUT_DIR
    global OUTPUT_DIR
    global BACKUPS_DIR
    global parser
    global ARGS
    INPUT_DIR = None
    OUTPUT_DIR = None
    BACKUPS_DIR = None
    parser = None
    ARGS = None
