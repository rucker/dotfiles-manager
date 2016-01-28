# dotfiles
These are my dotfiles. There are many like them, but these are mine.

This repo contains my dotfiles and a build script. The script will compile/symlink them and do some basic setup.

## Background
My dotfiles reached a point where they became complex enough that I didn't want to manage them by hand any more: not only do I want different things in .bashrc on Linux than I do in .bash_profile on OS X, but also I want to avoid accidentally committing any sensitive data they might contain to GitHub.

To those ends, I wrote a Python script that will manage my dotfiles for me.

## Goals

The goals of this project are:  
1. Compile dotfiles from external files as needed (e.g. .bashrc/.bash_profile as described above).  
2. Easily maintain various other config files (e.g. vimrc) that don't need this compilation. For those files, create the appropriate symlinks from <code>~</code> to this project's location.  
3. Be portable to various NIX-like systems. The project should work correctly regardless of where it lives on disk (it should not have any hard-coded paths). I may get it working on Windows/Cygwin if I ever get stuck doing development on that platform.  

## Usage
<code>$ ./dotfiles/dotfiles.py</code>
This will:
* Symlink <code>~/.vimrc -> ./vimrc</code>
* Create a platform-specific bash dotfile in <code>~</code>
* Symlink <code>~/.gitconfig -> ./gitconfig</code>

## Compiled Dotfiles

The dotfiles are compiled from the input files described below, which are located in <code>./dotfiles/inputfiles</code>:

### bashrc/bash_profile

##### bash_common
Contains any elements common across platforms.

##### bash_private (optional)
Contains any sensitive data that should not be committed to version control.

##### bash_linux
Contains any elements specific to Linux.

##### bash_mac
Contains any elements specific to Mac OS X.

### gitconfig

##### git_public
Contains any tokens that can be made public (e.g. published on GitHub)

##### git_private (optional)
Contains private tokens that should not be shared (e.g. personal keys)

## The scripts directory
The scripts directory can be used to incorporate additional scripts into the user's bash session. The scripts directory contains the following subdirectories:

### sourced
Scripts in this directory will be sourced when `.bashrc/.bash_profile` is sourced. 

### sourced-private (optional)
Same as above, except that scripts in this directory will be ignored by git.

## Dependencies
The <code>mock</code> and <code>enum34</code> packages are required. Fetch them from PyPi using pip, i.e. <code>$ pip install mock enum34</code>

For the Mac version, a Homebrew installation is assumed as is using GNU Bash.

## FAQ
**Q**: The script creates bashrc/bash_profile and .bashrc/.bash_profile. Why two versions of each?  
**A**: bashrc/bash_profile are what I commit to GitHub. They are for show. These files do not contain the contents of bash_private, whereas their dotted counterparts do.  
**Q**: I deleted a file and now the script fails. What gives?  
**A**: Anything in the .gitignore file is considered optional. Everything else is considered required. Renaming or removing anything not git-ignored will cause problems.

## TO DO / Wishlist
- Allow an entry in bash_private to override an identical entry from another file under version control. Example: On a specific machine, I might want to export a custom PS1. This should override/take precedence (and ideally, it should replace the existing entry if it's already been compiled to an output file).
- Implement -v / --verbose switch (possibly implement logging for this).
- Incorporate [testfixtures](https://pythonhosted.org/testfixtures/index.html) package into tests ([TempDir](https://pythonhosted.org/testfixtures/files.html) in particular).
