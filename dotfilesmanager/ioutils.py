import io
import os
import sys
from os.path import join
import time
import glob
import shutil

from dotfilesmanager import env
from dotfilesmanager.constants import SRCFILES, DOTFILES


def output(str):
    if env.ARGS.verbose:
        print(str)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_file(file_name, contents):
    with open(file_name, 'w') as file:
        file.write(contents)


def destroy_file(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)


def compile_dotfile(file_name):
    output("Compiling file: " + file_name)
    with io.StringIO() as file_buffer:
        input_file_name = file_name.replace('.', '')
        write_required_input_file_contents(input_file_name + "_global", file_buffer)
        if not env.ARGS.no_local:
            write_optional_input_file_contents(
                input_file_name + "_local", file_buffer)
        write_output_file(join(env.OUTPUT_DIR, file_name), file_buffer)
        output("File completed.\n")


def backup_file(file_name):
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    bak_file = join(
        env.BACKUPS_DIR,
        file_name[file_name.rfind('/') + 1:]
        .replace('.', '') + '_' +
        timestamp + '.bak')
    output("\tBacking up " + file_name + " to " + bak_file)
    if not os.path.exists(env.BACKUPS_DIR):
        os.mkdir(env.BACKUPS_DIR)
    shutil.move(file_name, bak_file)


def write_optional_input_file_contents(file_name, file_buffer):
    if os.path.isfile(join(env.INPUT_DIR, file_name)):
        write_input_file_contents(file_name, file_buffer)
    else:
        output("\t" + file_name + " is not present. Skipping...")


def write_required_input_file_contents(file_name, file_buffer):
    if os.path.isfile(join(env.INPUT_DIR, file_name)):
        write_input_file_contents(file_name, file_buffer)
    else:
        msg = "Required input file " + file_name + \
            " is not present. Please replace the file and try again."
        if env.ARGS.verbose:
            msg = "\t" + msg
        eprint(msg)
        exit(1)


def write_input_file_contents(file_name, file_buffer):
    with open(join(env.INPUT_DIR, file_name)) as input_file:
        output("\tReading input file " + file_name)
        for line in input_file:
            write_to_output_buffer(line, file_buffer)


def write_output_file(file_path, file_buffer):
    if not env.ARGS.clobber and os.path.isfile(file_path):
        backup_file(file_path)
    output("\tWriting output file " + file_path)
    with open(file_path, 'w') as output_file:
        output_file.write(file_buffer.getvalue())


def write_to_output_buffer(output, file_buffer):
    file_buffer.write(str(output))


def revert_dotfiles(file_names):
    for dotfile in file_names:
        revert_dotfile(dotfile)


def revert_dotfile(dotfile):
    name = dotfile.replace('.', '')
    search_pattern = '{0}*{1}*'.format(env.BACKUPS_DIR, name)
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
