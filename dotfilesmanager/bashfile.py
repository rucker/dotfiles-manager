import io
from os.path import join

from dotfilesmanager import env
from dotfilesmanager import ioutils
from dotfilesmanager.constants import SYSTEMS, BASHFILES


def _write_header(file_name, file_buffer):
    header = ("#!/bin/bash\n# ~/{0}"
    ": executed by bash(1) for non-login shells.\n"
    "# This file was generated by a script. Do not edit manually!\n\n"
    .format(file_name))
    ioutils.write_to_output_buffer(header, file_buffer)


def compile_bash_file(platform):
    if platform == SYSTEMS.DARWIN.value:
        bash_file = BASHFILES.BASH_PROFILE.value
        if env.IS_GNU:
            bash_platform_file = BASHFILES.BASH_MAC_GNU.value
        else:
            bash_platform_file = BASHFILES.BASH_MAC_BSD.value
    elif platform == SYSTEMS.LINUX.value:
        bash_file = BASHFILES.BASHRC.value
        bash_platform_file = BASHFILES.BASH_LINUX.value

    ioutils.sprint("Compiling file: " + bash_file)
    with io.StringIO() as file_buffer:
        _write_header(bash_file, file_buffer)
        ioutils.write_input_file_contents(
            BASHFILES.BASH_GLOBAL.value, file_buffer)
        ioutils.write_input_file_contents(bash_platform_file, file_buffer)
        if not env.ARGS.no_local:
            ioutils.write_input_file_contents(
                BASHFILES.BASH_LOCAL.value, file_buffer)
        ioutils.write_output_file(join(env.OUTPUT_DIR, bash_file), file_buffer)
        ioutils.sprint("File completed.\n")


def compile_bash_profile():
    compile_bash_file(SYSTEMS.DARWIN.value)


def compile_bashrc():
    compile_bash_file(SYSTEMS.LINUX.value)
