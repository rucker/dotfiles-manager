#!/usr/bin/env python3

import argparse
import itertools
import os
import re
import sys
from argparse import Namespace
from collections.abc import Iterator
from importlib.metadata import version

from dotfilesmanager.config import Config
from dotfilesmanager.ioutils import ioutils


def _get_version() -> str:
    """Get package version from metadata."""
    try:
        return version("dotfiles-manager")
    except Exception:
        return "unknown"


def _parse_args() -> Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Compile various dotfiles using their input files."
    )
    parser.add_argument("input_dir", default=None, help="input files directory")
    parser.add_argument(
        "-c",
        "--clobber",
        action="store_true",
        help="Clobber any existing output files (don't back them up).",
    )
    parser.add_argument(
        "-r",
        "--revert",
        action="store_true",
        help="Revert dotfiles to most recent backup.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {_get_version()}")
    parser.add_argument(
        "-o",
        "--output-dir",
        nargs=1,
        help="Specify output directory (default value is $HOME).",
    )
    parser.add_argument("-f", "--file", nargs=1, help="Process only the specified dotfile.")
    parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        action="append",
        metavar="INPUT_FILE",
        help="Exclude the specified input file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write anything to disk, but instead report what "
        "action(s) would be taken. Implies --verbose.",
    )
    parser.add_argument(
        "--no-symlinks",
        action="store_true",
        help="Don't symlink output dotfiles (compile a new file instead)",
    )

    args = parser.parse_args()

    # Print startup message
    if args.verbose or args.dry_run:
        print("\nPreparing dotfiles with args: " + " ".join(sys.argv[1:]) + "\n")

    return args


def _print_env_info(config: Config) -> None:
    """Print environment configuration if verbose mode is enabled."""
    if config.verbose:
        print("Environment:")
        print(f"\tinput_dir: {config.input_dir}")
        print(f"\tbackups_dir: {config.backups_dir}")
        print(f"\toutput_dir: {config.output_dir}")
        print(f"\targs: {config.args}\n")


def _print_completion_message(config: Config, processed_dotfiles: list[str]) -> None:
    """Print completion message with list of processed dotfiles."""
    if config.verbose:
        pretty_list = ", ".join(processed_dotfiles)
        print(f"Processed the following dotfiles: {pretty_list}")


def _sort_input_file_list(input_files: list[str]) -> list[str]:
    """Sort input files by priority number (99- prefix) then alphabetically."""
    to_sort = []
    not_to_sort = []
    for file_name in input_files:
        if not re.search(r"[0-9]{2}\-", file_name):
            not_to_sort.append(file_name)
        else:
            to_sort.append(file_name)
    result = sorted(to_sort, reverse=True)
    result.extend(not_to_sort)
    return result


def _get_dotfile_name(file_name: str) -> str:
    """Extract dotfile name from input filename using naming convention.

    For nested paths (containing '/'), the naming convention is applied only to
    the filename component, while the directory path is preserved as-is.

    Examples:
        'bashrc' -> '.bashrc'
        '99-bashrc_local' -> '.bashrc'
        '.config/nvim/init.vim' -> '.config/nvim/init.vim'
        '.config/nvim/99-init.vim_local' -> '.config/nvim/init.vim'
    """
    # Split into directory and filename components
    if "/" in file_name:
        dir_part, base_name = file_name.rsplit("/", 1)
    else:
        dir_part = ""
        base_name = file_name

    # Apply naming convention to base filename
    if "-" in base_name:
        sidx = base_name.index("-") + 1
    else:
        sidx = 0
    if "_" in base_name:
        eidx = base_name.index("_")
    else:
        eidx = len(base_name)
    if eidx < sidx:
        sidx = 0

    processed_name = base_name[sidx:eidx]

    # For nested paths, preserve directory path as-is
    # For top-level files, add leading dot
    if dir_part:
        dotfile_name = f"{dir_part}/{processed_name}"
    else:
        dotfile_name = "." + processed_name

    return dotfile_name


def _is_input_file_excluded(config: Config, file_name: str) -> bool:
    """Check if input file should be excluded based on config."""
    if not config.args.exclude:
        return False
    all_excludes = list(itertools.chain.from_iterable(config.args.exclude))
    normalized_excludes = [os.path.normpath(item) for item in all_excludes]
    return file_name in normalized_excludes


def _is_binary_file(config: Config, file_name: str) -> bool:
    """Check if a file is binary by looking for null bytes in its content."""
    file_path = os.path.join(str(config.input_dir), file_name)

    # Skip if not a regular file
    if not os.path.isfile(file_path):
        return False

    try:
        # Read first 8KB to detect binary content
        with open(file_path, "rb") as f:
            chunk = f.read(8192)
            # Check for null byte, a strong indicator of binary content
            return b"\x00" in chunk
    except OSError:
        # If we can't read it, treat it as binary to be safe
        return True


def _add_input_file_to_dict(
    config: Config, dotfiles_dict: dict[str, list[str]], input_file: str
) -> None:
    """Add input file to dotfiles dictionary if not excluded or binary."""
    if _is_input_file_excluded(config, input_file):
        return

    if _is_binary_file(config, input_file):
        if config.verbose:
            print(f"Skipping binary file: {input_file}")
        return

    file_key = _get_dotfile_name(input_file)
    if file_key in dotfiles_dict:
        dotfiles_dict[file_key].append(input_file)
    else:
        dotfiles_dict[file_key] = [input_file]


def _walk_input_dir(config: Config) -> Iterator[str]:
    """Walk input directory recursively, yielding relative file paths."""
    for root, dirs, files in os.walk(config.input_dir):
        # Skip the backups directory
        if "backups" in dirs:
            dirs.remove("backups")
        for file_name in files:
            full_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(full_path, config.input_dir)
            yield rel_path


def _get_dotfiles_dict(config: Config) -> dict[str, list[str]]:
    """Build dictionary of dotfiles and their input files."""
    dotfiles: dict[str, list[str]] = {}

    for input_file in _walk_input_dir(config):
        _add_input_file_to_dict(config, dotfiles, input_file)
    for dotfile in dotfiles:
        dotfiles[dotfile] = _sort_input_file_list(dotfiles[dotfile])
    return dotfiles


def _process_dotfile(config: Config, dotfile: str, input_files: list[str]) -> None:
    """Process a single dotfile by compiling or symlinking."""
    if config.verbose:
        print("Processing file: " + dotfile)

    if config.args.no_symlinks or len(input_files) > 1:
        ioutils.compile_dotfile(config, dotfile, input_files)
    else:
        ioutils.create_symlink(
            config,
            str(config.input_dir / input_files[0]),
            str(config.output_dir / dotfile),
        )

    if config.verbose:
        print(f"Done with {dotfile}\n")


def _process_dotfiles(config: Config, all_dotfiles_dict: dict[str, list[str]]) -> None:
    """Process all dotfiles in the dictionary."""
    for dotfile in all_dotfiles_dict:
        _process_dotfile(config, dotfile, all_dotfiles_dict[dotfile])


def _revert_dotfiles(config: Config, file_names: list[str]) -> None:
    """Revert dotfiles to their most recent backup."""
    for dotfile in file_names:
        ioutils.revert_dotfile(config, dotfile)


def main() -> None:
    """Main entry point for dotfiles manager."""
    args = _parse_args()
    config = Config.from_args(args)
    _print_env_info(config)

    processed_dotfiles: list[str] = []
    all_dotfiles_dict = _get_dotfiles_dict(config)

    if config.args.file:
        dotfile = os.path.normpath(config.args.file[0])
        if _is_input_file_excluded(config, config.args.file[0]):
            if config.verbose:
                print(f"Warning: Received -f/--file {dotfile} but it was excluded.")
        else:
            if not dotfile.startswith("."):
                dotfile = "." + dotfile
            if config.args.revert:
                ioutils.revert_dotfile(config, dotfile)
                processed_dotfiles.append(dotfile)
            else:
                if dotfile in all_dotfiles_dict:
                    _process_dotfile(config, dotfile, all_dotfiles_dict[dotfile])
                    processed_dotfiles.append(dotfile)
                else:
                    print(
                        f"No input files found for {dotfile}. Please double-check "
                        "the file name(s) and try again.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
    else:
        all_dotfiles = list(all_dotfiles_dict)
        if config.args.revert:
            _revert_dotfiles(config, all_dotfiles)
        else:
            _process_dotfiles(config, all_dotfiles_dict)
        processed_dotfiles.extend(all_dotfiles)

    _print_completion_message(config, processed_dotfiles)


if __name__ == "__main__":
    main()
