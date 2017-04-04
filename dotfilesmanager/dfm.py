#!/usr/bin/env python3

import platform
import sys
import os
from os.path import join
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotfilesmanager import bashfile
from dotfilesmanager import env
from dotfilesmanager import ioutils
from dotfilesmanager.constants import SYSTEMS, DOTFILES
from dotfilesmanager.ioutils import sprint, eprint


def _init():
    _identify_system()
    _set_args()
    _set_env()


def _identify_system():
    supported_platforms = [SYSTEMS.DARWIN.value, SYSTEMS.LINUX.value]
    env.PLATFORM = platform.system()
    if env.PLATFORM not in supported_platforms:
        eprint("System not supported!")
        exit(1)

    env.IS_GNU = bool(env.PLATFORM == SYSTEMS.LINUX.value or os.path.isdir(
        '/usr/local/opt/coreutils/libexec/gnubin/'))


def _set_args():
    env.parser = argparse.ArgumentParser(
        description="Compile various dotfiles using their input files.")
    env.parser.add_argument(
        'input_dir',
        nargs='?',
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
        '-n',
        '--no-local',
        action='store_true',
        help="Skip _local input files during compilation.")
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
    env.ARGS = env.parser.parse_args()
    sprint("\nPreparing dotfiles with args: " + " ".join(sys.argv[1:]) + "\n")


def _set_env():
    if env.ARGS.input_dir:
        input_dir = env.ARGS.input_dir
        if os.path.isdir(input_dir):
            env.INPUT_DIR = input_dir
        else:
            eprint("Specified input directory " + input_dir + " does not " \
            "exist.")
            exit(1)
    else:
        env.parser.print_help()
        exit(1)
    if env.ARGS.output_dir:
        env.OUTPUT_DIR = env.ARGS.output_dir[0]
    env.BACKUPS_DIR = join(env.INPUT_DIR, 'backups')

    sprint("Environment:")
    sprint("\tplatform: " + env.PLATFORM)
    sprint("\tinput_dir: " + env.INPUT_DIR)
    sprint("\tbackups_dir: " + env.BACKUPS_DIR)
    sprint("\toutput_dir: " + env.OUTPUT_DIR)
    sprint("\targs: " + str(env.ARGS))
    sprint("")


def _print_completion_message():
    if env.PLATFORM == SYSTEMS.DARWIN.value:
        bash_file_name = DOTFILES.BASH_PROFILE.value
    else:
        bash_file_name = DOTFILES.BASHRC.value
    print("Done. Recommend you source ~/{0} or start new a terminal session."\
        .format(bash_file_name))


def main():
    _init()
    if env.ARGS.file:
        dotfile = env.ARGS.file[0]
        if not dotfile.startswith("."):
            dotfile = "." + dotfile
        if env.ARGS.revert:
            ioutils.revert_dotfile(dotfile)
        else:
            if dotfile == DOTFILES.BASHRC.value:
                bashfile.compile_bashrc()
            elif dotfile == DOTFILES.BASH_PROFILE.value:
                bashfile.compile_bash_profile()
            elif dotfile == DOTFILES.VIMRC.value:
                ioutils.compile_dotfile(DOTFILES.VIMRC.value)
            elif dotfile == DOTFILES.GITCONFIG.value:
                ioutils.compile_dotfile(DOTFILES.GITCONFIG.value)
            else:
                dotfiles = str([df.value for df in DOTFILES])
                eprint(
                    "{0} is not a recognized dotfile. \
                    Valid dotfile names are: {1}"
                    .format(dotfile, dotfiles))
                exit(1)
    else:
        if env.ARGS.revert:
            ioutils.revert_dotfiles([df.value for df in DOTFILES])
        else:
            bashfile.compile_bash_file(env.PLATFORM)
            ioutils.compile_dotfile(DOTFILES.VIMRC.value)
            ioutils.compile_dotfile(DOTFILES.GITCONFIG.value)
    _print_completion_message()

if __name__ == '__main__':
    main()
