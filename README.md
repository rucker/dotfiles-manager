# dotfiles
These are my dotfiles. There are many like them, but these are mine.

This repo contains my dotfiles and a build script. The script will compile/symlink them and do some basic setup.

## What it Does
Running <code>$ ./dotfiles/dotfiles.py</code> will:
* Back up any existing dotfiles to `./dotfiles/backups/`
* Symlink <code>~/.vimrc -> ./vimrc</code>
* Compile a platform-specific bash dotfile (i.e. `.bashrc` or `.bash_profile`), located in `$HOME`. By default, you'll get the latest version of my dotfiles unless you modify the relevant input files (below).
* Compile a `.gitconfig file`, located in `$HOME`

Use `$ dotfiles.py -h` for help.

## Background
My dotfiles reached a point where they became complex enough that I didn't want to manage them by hand any more: not only do I want different things in .bashrc on Linux than I do in .bash_profile on OS X, but also I want to avoid accidentally committing any sensitive data they might contain to GitHub.

To those ends, I wrote a Python script that will manage my dotfiles for me.  The goals of this project are: 
 
1. Compile dotfiles from external files as needed (e.g. .bashrc/.bash_profile as described above).  
2. Easily maintain various other config files (e.g. vimrc) that don't need this compilation. For those files, create the appropriate symlinks from `$HOME` to this project's location.  
3. Be portable to various NIX-like systems. The project should work correctly regardless of where it lives on disk (it should not have any hard-coded paths). I may get it working on Windows/Cygwin if I ever get stuck doing development on that platform.  

## Compiled Dotfiles

Both .gitconfig and .bashrc/.bash_profile are compiled from input files located in `./dotfiles/inputfiles`. Make note that the presence of most of these files is **required**.

### bashrc/bash_profile
Any Tokens contained in input files described below are compiled into bashrc/bash_profile in the following order:  
1. bash_common  
2. bash_$PLATFORM (i.e. `bash_linux`, `bash_mac_gnu`, or `bash_mac_bsd`). **One** of those three is required (see below)  
3. bash_private  
Be mindful of the order, particularly if you plan to make changes to your `$PATH`

**bash_common**  
Contains any elements common across platforms.

**bash_linux**  
Contains any elements specific to Linux.

**bash_mac_bsd**  
Contains any elements specific to Mac OS X systems where the BSD coreutils are used. If you're on a Mac and you're not sure what this means, you should probably use this file instead of `bash_mac_gnu`.

**bash_mac_gnu**  
Contains any elements specific to Mac OS X systems where the GNU coreutils are installed.

**bash_private (optional)**  
Contains any sensitive data that should not be committed to version control.

### gitconfig

**git_public**  
Contains any tokens that can be made public (e.g. published on GitHub)

**git_private (optional)**  
Contains private tokens that should not be shared (e.g. personal keys)

## The scripts directory
The scripts directory can be used to incorporate additional scripts into the user's bash session. The scripts directory contains the following subdirectories:

**sourced**  
Scripts in this directory will be sourced when `.bashrc/.bash_profile` is sourced. 

**sourced-private (optional)**  
Same as above, except that scripts in this directory will be ignored by git.

## Dependencies
The <code>mock</code> and <code>enum34</code> packages are required. Fetch them from PyPi using pip, i.e. <code>$ pip install mock enum34</code>

For the Mac version, a Homebrew installation is assumed as is using the GNU coreutils.

## Testing  
Everything in this project is test-driven. `$ testdriver.py` will run all tests.  
Unit tests: Exercise logic e.g. execution path.  
Integration tests: Deal with file IO. Env paths are altered so as not to break 'prod' data (the real text files).

## FAQ
**Q**: Why are there two input files for Mac systems (`bash_mac_gnu` and `bash_mac_bsd`)?  
**A**: The intention is for this build script **and** any dotfiles it creates to be portable to various sytems. At the time of this writing, I use the GNU coreutils on my personal Macbook. As such, I have a few aliases that are not compatible with Mac systems that *don't* use the GNU coreutils (read: most of them). So if I were to run the build script on another Mac system, I don't want anything incompatible to wind up in my dotfiles there.  
**Q**: The script creates `bashrc/bash_profile` and `.bashrc/.bash_profile`. Why two versions of each?  
**A**: bashrc/bash_profile are what I commit to GitHub. They are for show. These files do not contain the contents of bash_private, whereas their dotted counterparts do.  
**Q**: I deleted/moved/renamed a file and now the script fails. What gives?  
**A**: Input files that are core to this script's functionality are considered to be required. Removing or renaming those files will cause problems.  
**Q**: If this script is for managing dotfiles, why are you keeping and sourcing external scripts?  
**A**: The idea is for those scripts' functionality to be availble during my bash session. Since I could produce the same effect by writing the contents of those scripts to `.bashrc/.bash_profile`, I think this is still in the spirit of managing my dotfiles.

## TO DO / Wishlist
- Add `-y --yes-to-all` switch. Would be useful e.g. `$ dotfiles -ry`
- Give user the ability to pass in specific dotfile(s) for compilation. Could be done via `-f --file` switch.
- Incorporate [testfixtures](https://pythonhosted.org/testfixtures/index.html) package into tests ([TempDir](https://pythonhosted.org/testfixtures/files.html) in particular).  
- Get a proper sdist and install working via setup.py. Part of this is making sense of ["Specify testfixtures in the tests_require parameter of your package’s call to setup in setup.py."](https://pythonhosted.org/testfixtures/installation.html) once `testfixtures` has been implemented.
  - Part of this could be creating necessary directories such as `backups` (which would allow that dir and its .gitignore to be removed from git).
- Migrate to Python 3.
