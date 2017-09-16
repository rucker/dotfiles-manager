import io
import os
from os.path import join, isfile
import sys
import time
import glob
import shutil

from dotfilesmanager import env
from dotfilesmanager.constants import BASHFILES


def sprint(message):
    if env.ARGS.verbose:
        print(message)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_file(file_name, contents):
    with open(file_name, 'w') as file:
        file.write(contents)


def destroy_file(file_name):
    if isfile(file_name):
        os.remove(file_name)


def backup_file(file_name):
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

def get_dotfile_name(file_name):
    if '_' in file_name:
        file_name = file_name[0:file_name.index('_')]
    if file_name in [item.value for item in BASHFILES]:
        return None
    return '.' + file_name


def get_dotfiles_map(input_dir):
    dotfiles = {}
    for item in os.listdir(input_dir):
        if os.path.isfile(join(input_dir, item)):
            file_key = get_dotfile_name(item)
            if file_key is not None:
                if file_key in dotfiles:
                    dotfiles[file_key].append(item)
                else:
                    dotfiles[file_key] = [item]
    return dotfiles


def compile_dotfiles(input_dir):
    for dotfile in iter(get_dotfiles_map(input_dir)):
        compile_dotfile(dotfile)


def compile_dotfile(file_name):
    with io.StringIO() as file_buffer:
        if file_name.startswith('.'):
            input_file_name = file_name[1:]
        else:
            input_file_name = file_name
        sprint("Compiling file: " + file_name)
        write_input_file_contents(input_file_name, file_buffer)
        if not env.ARGS.no_local:
            write_input_file_contents(
                input_file_name + "_local", file_buffer)
        write_output_file(join(env.OUTPUT_DIR, file_name), file_buffer)
        sprint("File completed.\n")


def write_input_file_contents(file_name, out_buffer):
    file_name_with_path = join(env.INPUT_DIR, file_name)
    if not isfile(file_name_with_path):
        sprint("{0} is not present. Skipping...".format(file_name_with_path))
        return
    with open(file_name_with_path) as input_file:
        sprint("\tReading input file " + file_name)
        try:
            for line in input_file:
                write_to_output_buffer(line, out_buffer)
        except UnicodeDecodeError:
            eprint("Input file {0} is not a valid UTF-8 file. Skipping..."
                .format(input_file))


def write_output_file(file_path, contents):
    if not env.ARGS.clobber and isfile(file_path):
        backup_file(file_path)
    sprint("\tWriting output file " + file_path)
    with open(file_path, 'w') as output_file:
        output_file.write(contents.getvalue())


def write_to_output_buffer(output, file_buffer):
    file_buffer.write(str(output))


def revert_dotfiles(file_names):
    for dotfile in file_names:
        revert_dotfile(dotfile)


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