import glob
import io
import os
from os.path import join, isfile
import shutil
import sys
import time

from dotfilesmanager import env


def sprint(message):
    if env.ARGS.verbose:
        print(message)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _create_file(file_name, contents):
    with open(file_name, 'w') as file:
        file.write(contents)


def _back_up_file(file_name):
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    bak_file = join(
        env.BACKUPS_DIR,
        file_name[file_name.rfind('/') + 1:]
        .replace('.', '') + '_' +
        timestamp + '.bak')
    sprint("\tBacking up " + file_name + " to " + bak_file)
    if not os.path.exists(env.BACKUPS_DIR):
        os.mkdir(env.BACKUPS_DIR)
    shutil.move(file_name, bak_file)


def compile_dotfile(file_name, input_files):
    with io.StringIO() as file_buffer:
        sprint("Compiling file: " + file_name)
        for input_file in input_files:
            _write_input_file_contents(input_file, file_buffer)
        _write_output_file(join(env.OUTPUT_DIR, file_name), file_buffer)
        sprint("File completed.\n")


def _write_input_file_contents(file_name, out_buffer):
    file_name_with_path = join(env.INPUT_DIR, file_name)
    if not isfile(file_name_with_path):
        sprint("{0} is not present. Skipping...".format(file_name_with_path))
        return
    with open(file_name_with_path) as input_file:
        sprint("\tReading input file " + file_name)
        try:
            for line in input_file:
                _write_to_output_buffer(line, out_buffer)
        except UnicodeDecodeError:
            sprint("Input file {0} is not a valid UTF-8 file. Skipping..."
                .format(input_file))


def _write_output_file(file_path, contents):
    if not env.ARGS.clobber and isfile(file_path):
        _back_up_file(file_path)
    sprint("\tWriting output file " + file_path)
    with open(file_path, 'w') as output_file:
        output_file.write(contents.getvalue())


def _write_to_output_buffer(output, file_buffer):
    file_buffer.write(str(output))


def revert_dotfile(dotfile):
    name = '*{0}*'.format(dotfile).replace('.', '')
    search_pattern = join(env.BACKUPS_DIR, name)
    results = sorted(glob.glob(search_pattern), reverse=True)
    if results:
        bak_file = results[0]
        choice = ''
        while choice not in (['Y', 'N']):
            choice = input(
                "Revert {0} to backup located at {1}? (Y/N): "
                .format(dotfile, bak_file)).upper()
            if choice == 'Y':
                os.remove(join(env.OUTPUT_DIR, dotfile))
                shutil.copy(bak_file, join(env.OUTPUT_DIR, dotfile))
    else:
        eprint("No backup files found matching {0}".format(dotfile))
