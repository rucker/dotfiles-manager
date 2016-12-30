import os
from os.path import join

from constants import MISC

ARGS = ''
HOME = os.environ['HOME']
PLATFORM = ''
INPUT_DIR = ''
OUTPUT_DIR = HOME
BACKUPS_DIR = ''
IS_GNU = ''
CONFIG_FILE = join(HOME, MISC.CONFIG_FILE.value)
