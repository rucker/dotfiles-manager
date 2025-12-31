import glob
import io
import os
import shutil
import sys
import time
from os.path import basename, exists, isdir, isfile, islink, join, lexists, normpath
from typing import Any, TextIO

from dotfilesmanager.config import Config


def prints(config: Config, message: str) -> None:
    """Print message if verbose mode is enabled."""
    if config.verbose:
        print(message)


def printe(*args: object, **kwargs: Any) -> None:
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def _create_file(config: Config, file_name: str, contents: str) -> None:
    """Create a file with given contents."""
    prints(config, f"Writing to file: {file_name}")
    if not config.dry_run:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(contents)


def _back_up(config: Config, file_path: str) -> None:
    """Back up a file to the backups directory with timestamp."""
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = basename(file_path)
    bak_file = join(
        str(config.backups_dir),
        (filename.replace(".", "", 1) if filename.startswith(".") else filename)
        + "_"
        + timestamp
        + ".bak",
    )

    if not exists(str(config.backups_dir)):
        prints(config, f"Creating backups dir {config.backups_dir}")
        if not config.dry_run:
            os.mkdir(str(config.backups_dir))

    prints(config, f"\tBacking up {file_path} to {bak_file}")
    if not config.dry_run:
        shutil.move(os.readlink(file_path) if islink(file_path) else file_path, bak_file)


def compile_dotfile(config: Config, file_name: str, input_files: list[str]) -> None:
    """Compile multiple input files into a single dotfile."""
    with io.StringIO() as file_buffer:
        for input_file in input_files:
            _write_input_file_contents(config, input_file, file_buffer)
        _write_output_file(config, join(str(config.output_dir), file_name), file_buffer)


def _write_input_file_contents(config: Config, file_name: str, out_buffer: TextIO) -> None:
    """Read input file and write its contents to the output buffer."""
    file_name_with_path = join(str(config.input_dir), file_name)
    if not isfile(file_name_with_path):
        prints(config, f"{file_name_with_path} is not present. Skipping...")
        return
    with open(file_name_with_path, encoding="utf-8") as input_file:
        prints(config, "\tReading input file " + file_name)
        try:
            for line in input_file:
                _write_to_output_buffer(line, out_buffer)
        except UnicodeDecodeError:
            prints(config, f"Input file {input_file} is not a valid UTF-8 file. Skipping...")


def _write_output_file(config: Config, file_path: str, contents: io.StringIO) -> None:
    """Write the compiled contents to the output file."""
    if islink(file_path):
        _remove_symlink(config, file_path)
    if not config.clobber and isfile(file_path):
        _back_up(config, file_path)
    prints(config, "\tWriting input file contents to output file " + file_path)
    if not config.dry_run:
        with open(file_path, "w", encoding="utf-8") as output_file:
            output_file.write(contents.getvalue())


def _write_to_output_buffer(output: str, file_buffer: TextIO) -> None:
    """Write a string to the output buffer."""
    file_buffer.write(str(output))


def revert_dotfile(config: Config, dotfile: str) -> None:
    """Revert a dotfile to its most recent backup."""
    name = f"*{dotfile}*".replace(".", "")
    search_pattern = join(str(config.backups_dir), name)
    results = sorted(glob.glob(search_pattern), reverse=True)
    if results:
        bak_file = results[0]
        choice = ""
        while choice not in (["Y", "N"]):
            choice = input(
                f"Revert {join(str(config.output_dir), dotfile)}"
                f"to backup located at {bak_file}? (Y/N): "
            ).upper()
            if choice == "Y":
                existing_dotfile = join(str(config.output_dir), dotfile)
                if not config.dry_run:
                    if isfile(existing_dotfile):
                        os.remove(existing_dotfile)
                        shutil.copy(bak_file, join(str(config.output_dir), dotfile))
                    elif isdir(existing_dotfile):
                        shutil.rmtree(existing_dotfile)
                        shutil.copytree(bak_file, join(str(config.output_dir), dotfile))
                print("Reverted.")
            else:
                print("Revert canceled.")
    else:
        printe(f"No backup files found matching {dotfile}")


def create_symlink(config: Config, target: str, source: str) -> None:
    """Create a symlink from source to target."""
    if lexists(source):
        existing_target = normpath(os.readlink(source))
        if not exists(existing_target):
            prints(config, f"\tExisting symlink {source} -> {existing_target} is broken")
            _remove_symlink(config, source)
        if target == existing_target:
            prints(config, f"\tSymlink {source} -> {target} already in place")
            return
        _back_up(config, source)
    prints(config, f"\tSymlinking {source} -> {target}")
    if not config.dry_run:
        os.symlink(target, source)


def _remove_symlink(config: Config, link: str) -> None:
    """Remove a symlink."""
    prints(config, "\tRemoving symlink " + link)
    if not config.dry_run:
        os.unlink(link)
