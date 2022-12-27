import glob
import io
import os
from os.path import join, isfile, islink, exists, lexists, normpath
import shutil
import sys
import time

from env import env


def prints(message):
    if env.ARGS.verbose:
        print(message)


def printe(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _create_file(file_name, contents):
    prints(f"Writing to file: {file_name}")
    if not env.ARGS.dry_run:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(contents)


def _back_up(file_name):
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    bak_file = join(
        env.BACKUPS_DIR,
        file_name[file_name.rfind(os.sep) + 1:]
        .replace('.', '') + '_' +
        timestamp + '.bak')
    if not exists(env.BACKUPS_DIR):
        prints(f"Creating backups dir {env.BACKUPS_DIR}")
        if not env.ARGS.dry_run:
            os.mkdir(env.BACKUPS_DIR)
    prints(f"\tBacking up {file_name} to {bak_file}")
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
        prints(f"{file_name_with_path} is not present. Skipping...")
        return
    with open(file_name_with_path, encoding='utf-8') as input_file:
        prints("\tReading input file " + file_name)
        try:
            for line in input_file:
                _write_to_output_buffer(line, out_buffer)
        except UnicodeDecodeError:
            prints(f"Input file {input_file} is not a valid UTF-8 file. Skipping...")


def _write_output_file(file_path, contents):
    if islink(file_path):
        _remove_symlink(file_path)
    if not env.ARGS.clobber and isfile(file_path):
        _back_up(file_path)
    prints("\tWriting input file contents to output file " + file_path)
    if not env.ARGS.dry_run:
        with open(file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(contents.getvalue())


def _write_to_output_buffer(output, file_buffer):
    file_buffer.write(str(output))


def revert_dotfile(dotfile):
    name = f'*{dotfile}*'.replace('.', '')
    search_pattern = join(env.BACKUPS_DIR, name)
    results = sorted(glob.glob(search_pattern), reverse=True)
    if results:
        bak_file = results[0]
        choice = ''
        while choice not in (['Y', 'N']):
            choice = input(
                f"Revert {dotfile} to backup located at {bak_file}? (Y/N): ").upper()
            if choice == 'Y':
                existing_dotfile = join(env.OUTPUT_DIR, dotfile)
                prints((f"Removing dotfile {existing_dotfile}"
                        f" and replacing with backup named {bak_file}"))
                if not env.ARGS.dry_run:
                    os.remove(existing_dotfile)
                    shutil.copy(bak_file, join(env.OUTPUT_DIR, dotfile))
    else:
        printe(f"No backup files found matching {dotfile}")


def create_symlink(target, source):
    if lexists(source):
        existing_target = normpath(os.readlink(source))
        if not exists(existing_target):
            prints(f"\tExisting symlink {source} -> {existing_target} is broken")
            _remove_symlink(source)
        if target == existing_target:
            prints(f"\tSymlink {source} -> {target} already in place")
            return
    _back_up(source)
    prints(f"\tSymlinking {source} -> {target}")
    if not env.ARGS.dry_run:
        os.symlink(target, source)


def _remove_symlink(link):
    prints("\tRemoving symlink " + link)
    if not env.ARGS.dry_run:
        os.unlink(link)
