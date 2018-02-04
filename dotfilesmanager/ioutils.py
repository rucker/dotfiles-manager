import glob
import io
import os
from os.path import join, isfile, islink, exists
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
    sprint("Writing to file: {0}".format(file_name))
    if not env.ARGS.dry_run:
        with open(file_name, 'w') as file:
            file.write(contents)


def _back_up_file(file_name):
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    bak_file = join(
        env.BACKUPS_DIR,
        file_name[file_name.rfind('/') + 1:]
        .replace('.', '') + '_' +
        timestamp + '.bak')
    if not exists(env.BACKUPS_DIR):
        sprint("Creating backups dir {0}".format(env.BACKUPS_DIR))
        if not env.ARGS.dry_run:
            os.mkdir(env.BACKUPS_DIR)
    sprint("\tBacking up {0} to {1}".format(file_name, bak_file))
    if not env.ARGS.dry_run:
        shutil.move(file_name, bak_file)


def compile_dotfile(file_name, input_files):
    with io.StringIO() as file_buffer:
        for input_file in input_files:
            _write_input_file_contents(input_file, file_buffer)
        _write_output_file(join(env.OUTPUT_DIR, file_name), file_buffer)


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
            sprint("Input file {0} is not a valid UTF-8 file. Skipping..." \
                .format(input_file))


def _write_output_file(file_path, contents):
    if islink(file_path):
        _remove_symlink(file_path)
    if not env.ARGS.clobber and isfile(file_path):
        _back_up_file(file_path)
    sprint("\tWriting input file contents to output file " + file_path)
    if not env.ARGS.dry_run:
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
                "Revert {0} to backup located at {1}? (Y/N): " \
                        .format(dotfile, bak_file)).upper()
            if choice == 'Y':
                existing_dotfile = join(env.OUTPUT_DIR, dotfile)
                sprint("Removing dotfile {0} and replacing with backup named {1}" \
                        .format(existing_dotfile, bak_file))
                if not env.ARGS.dry_run:
                    os.remove(existing_dotfile)
                    shutil.copy(bak_file, join(env.OUTPUT_DIR, dotfile))
    else:
        eprint("No backup files found matching {0}".format(dotfile))


def create_symlink(target, source):
    if exists(source):
        if isfile(source):
            _back_up_file(source)
        else:
            existing_target = os.readlink(source)
            if not isfile(existing_target):
                sprint("\tExisting symlink {0} -> {1} is broken"\
                        .format(source, existing_target))
                _remove_symlink(source)
            if target == existing_target:
                sprint("\tSymlink {0} -> {1} already in place"\
                        .format(source, target))
                return
    sprint("\tSymlinking {0} -> {1}".format(source, target))
    if not env.ARGS.dry_run:
        os.symlink(target, source)


def _remove_symlink(link):
    sprint("\tRemoving symlink " + link)
    if not env.ARGS.dry_run:
        os.unlink(link)
