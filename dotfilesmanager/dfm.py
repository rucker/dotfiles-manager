#!/usr/bin/env python3

import itertools
import re
import sys
import os
from os.path import join
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotfilesmanager import env
from dotfilesmanager import ioutils
from dotfilesmanager.ioutils import sprint, eprint


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
    env.ARGS = env.parser.parse_args()
    sprint("\nPreparing dotfiles with args: " + " ".join(sys.argv[1:]) + "\n")


def _set_env():
    input_dir = env.ARGS.input_dir
    if os.path.isdir(input_dir):
        env.INPUT_DIR = input_dir
    else:
        eprint("Specified input directory " + input_dir + " does not " \
        "exist.")
        exit(1)
    if env.ARGS.output_dir:
        env.OUTPUT_DIR = env.ARGS.output_dir[0]
    env.BACKUPS_DIR = join(env.INPUT_DIR, 'backups')

    sprint("Environment:")
    sprint("\tinput_dir: " + env.INPUT_DIR)
    sprint("\tbackups_dir: " + env.BACKUPS_DIR)
    sprint("\toutput_dir: " + env.OUTPUT_DIR)
    sprint("\targs: " + str(env.ARGS))
    sprint("")


def _print_completion_message(processed_dotfiles):
    pretty_list = ', '.join(processed_dotfiles)
    sprint("Processed the following dotfiles: {0}" \
            .format(pretty_list))


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
    return file_name in all_excludes


def _add_input_file_to_dict(dotfiles_dict, input_file):
    if not _is_input_file_excluded(input_file):
        file_key = _get_dotfile_name(input_file)
        if file_key in dotfiles_dict:
            dotfiles_dict[file_key].append(input_file)
        else:
            dotfiles_dict[file_key] = [input_file]


def _get_dotfiles_dict(input_dir):
    dotfiles = {}
    all_input_files = [item for item in os.listdir(input_dir) if os.path.isfile(join(input_dir, item))]
    for input_file in all_input_files:
        _add_input_file_to_dict(dotfiles, input_file)
    for dotfile in dotfiles:
        dotfiles[dotfile] = _sort_input_file_list(dotfiles[dotfile])
    return dotfiles


def _compile_dotfiles(all_dotfiles_dict):
    for dotfile in all_dotfiles_dict:
        ioutils.compile_dotfile(dotfile, all_dotfiles_dict[dotfile])


def _revert_dotfiles(file_names):
    for dotfile in file_names:
        ioutils.revert_dotfile(dotfile)


def main():
    _init()
    processed_dotfiles = []
    all_dotfiles_dict = _get_dotfiles_dict(env.INPUT_DIR)
    if env.ARGS.file:
        dotfile = env.ARGS.file[0]
        if not dotfile.startswith("."):
            dotfile = "." + dotfile
        if env.ARGS.revert:
            processed_dotfiles.append(dotfile)
            ioutils.revert_dotfile(dotfile)
        else:
            if dotfile in all_dotfiles_dict:
                processed_dotfiles.append(dotfile)
                ioutils.compile_dotfile(dotfile, all_dotfiles_dict[dotfile])
            else:
                eprint(
                    "No input files found for {0}. Please double-check " \
                     "the file name(s) and try again."
                    .format(dotfile))
                exit(1)
    else:
        all_dotfiles = [df for df in all_dotfiles_dict]
        processed_dotfiles.extend(all_dotfiles)
        if env.ARGS.revert:
            _revert_dotfiles(all_dotfiles)
        else:
            _compile_dotfiles(all_dotfiles_dict)
    _print_completion_message(processed_dotfiles)

if __name__ == '__main__':
    main()
