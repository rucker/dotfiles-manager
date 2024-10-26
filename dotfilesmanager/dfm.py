#!/usr/bin/env python3

import argparse
import itertools
import re
import sys
import os
from os.path import join

# Workaround - issue #55
if os.path.islink(__file__):
    sys.path[0] = os.path.dirname(os.readlink(__file__))
from env import env
from ioutils import ioutils
from ioutils.ioutils import prints, printe


def _init():
    _set_args()
    _set_env()


def _set_args():
    env.parser = argparse.ArgumentParser(
        description="Compile various dotfiles using their input files.")
    env.parser.add_argument(
        'input_dir',
        default=None,
        help="input files directory")
    env.parser.add_argument(
        '-c',
        '--clobber',
        action='store_true',
        help="Clobber any existing output files (don't back them up).")
    env.parser.add_argument(
        '-r',
        '--revert',
        action='store_true',
        help="Revert dotfiles to most recent backup.")
    env.parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help="Enable verbose output.")
    env.parser.add_argument(
        '-o',
        '--output-dir',
        nargs=1,
        help="Specify output directory (default value is $HOME).")
    env.parser.add_argument(
        '-f',
        '--file',
        nargs=1,
        help="Process only the specified dotfile.")
    env.parser.add_argument(
        '-e',
        '--exclude',
        nargs='+',
        action='append',
        metavar='INPUT_FILE',
        help="Exclude the specified input file.")
    env.parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Don't write anything to disk, but instead report what \
                action(s) would be taken. Implies --verbose.")
    env.parser.add_argument(
        '--no-symlinks',
        action='store_true',
        help="Don't symlink output dotfiles (compile a new file instead)")
    env.ARGS = env.parser.parse_args()
    prints("\nPreparing dotfiles with args: " + " ".join(sys.argv[1:]) + "\n")


def _set_env():
    input_dir = env.ARGS.input_dir
    if os.path.isdir(input_dir):
        env.INPUT_DIR = input_dir
    else:
        printe(f"Specified input directory {input_dir} does not exist.")
        sys.exit(1)
    if env.ARGS.output_dir:
        env.OUTPUT_DIR = env.ARGS.output_dir[0]
    if env.INPUT_DIR == env.OUTPUT_DIR:
        printe(f"INPUT_DIR {env.INPUT_DIR} cannot be the same as OUTPUT_DIR {env.OUTPUT_DIR}")
        sys.exit(1)
    env.BACKUPS_DIR = join(env.INPUT_DIR, 'backups')

    if env.ARGS.dry_run:
        env.ARGS.verbose = True

    prints("Environment:"
    f"\n\tinput_dir: {env.INPUT_DIR}"
    f"\n\tbackups_dir: {env.BACKUPS_DIR}"
    f"\n\toutput_dir: {env.OUTPUT_DIR}"
    f"\n\targs: {str(env.ARGS)}\n")


def _print_completion_message(processed_dotfiles):
    pretty_list = ', '.join(processed_dotfiles)
    prints(f"Processed the following dotfiles: {pretty_list}")


def _sort_input_file_list(input_files):
    to_sort = []
    not_to_sort = []
    for file_name in input_files:
        if not re.search(r'[0-9]{2}\-', file_name):
            not_to_sort.append(file_name)
        else:
            to_sort.append(file_name)
    result = sorted(to_sort, reverse=True)
    result.extend(not_to_sort)
    return result


def _get_dotfile_name(file_name):
    if '-' in file_name:
        sidx = file_name.index('-') + 1
    else:
        sidx = 0
    if '_' in file_name:
        eidx = file_name.index('_')
    else:
        eidx = len(file_name)
    if eidx < sidx:
        sidx = 0
    dotfile_name = '.' + file_name[sidx:eidx]
    return dotfile_name


def _is_input_file_excluded(file_name):
    if not env.ARGS.exclude:
        return False
    all_excludes = list(itertools.chain.from_iterable(env.ARGS.exclude))
    normalized_excludes = [os.path.normpath(item) for item in all_excludes]
    return file_name in normalized_excludes


def _add_input_file_to_dict(dotfiles_dict, input_file):
    if not _is_input_file_excluded(input_file):
        file_key = _get_dotfile_name(input_file)
        if file_key in dotfiles_dict:
            dotfiles_dict[file_key].append(input_file)
        else:
            dotfiles_dict[file_key] = [input_file]


def _get_dotfiles_dict(input_dir):
    dotfiles = {}

    for input_file in os.listdir(input_dir):
        _add_input_file_to_dict(dotfiles, input_file)
    for dotfile in dotfiles:
        dotfiles[dotfile] = _sort_input_file_list(dotfiles[dotfile])
    return dotfiles


def _process_dotfile(dotfile, input_files):
    prints("Processing file: " + dotfile)
    if env.ARGS.no_symlinks or len(input_files) > 1:
        ioutils.compile_dotfile(dotfile, input_files)
    else:
        ioutils.create_symlink(join(env.INPUT_DIR, input_files[0]),
                               join(env.OUTPUT_DIR, dotfile))
    prints(f"Done with {dotfile}\n")


def _process_dotfiles(all_dotfiles_dict):
    for dotfile in all_dotfiles_dict:
        _process_dotfile(dotfile, all_dotfiles_dict[dotfile])


def _revert_dotfiles(file_names):
    for dotfile in file_names:
        ioutils.revert_dotfile(dotfile)


def main():
    _init()
    processed_dotfiles = []
    all_dotfiles_dict = _get_dotfiles_dict(env.INPUT_DIR)
    if env.ARGS.file:
        dotfile = os.path.normpath(env.ARGS.file[0])
        if _is_input_file_excluded(env.ARGS.file[0]):
            prints(f"Warning: Received -f/--file {dotfile} but it was excluded.")
        else:
            if not dotfile.startswith("."):
                dotfile = "." + dotfile
            if env.ARGS.revert:
                ioutils.revert_dotfile(dotfile)
                processed_dotfiles.append(dotfile)
            else:
                if dotfile in all_dotfiles_dict:
                    _process_dotfile(dotfile, all_dotfiles_dict[dotfile])
                    processed_dotfiles.append(dotfile)
                else:
                    printe(
                        f"No input files found for {dotfile}. Please double-check "
                        "the file name(s) and try again.")
                    sys.exit(1)
    else:
        all_dotfiles = list(all_dotfiles_dict)
        if env.ARGS.revert:
            _revert_dotfiles(all_dotfiles)
        else:
            _process_dotfiles(all_dotfiles_dict)
        processed_dotfiles.extend(all_dotfiles)
    _print_completion_message(processed_dotfiles)

if __name__ == '__main__':
    main()
