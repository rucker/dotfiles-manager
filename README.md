# Dotfiles Manager
Dotfiles Manager allows for the compilation of dotfiles using a convention of named input files. A simple use-case might be:

`dfm.py ${INPUT_DIR}`

Where `${INPUT_DIR}` is the location of your [input files](#input-files).

See `dfm.py --help` for more information.

Existing dotfiles are backed up automatically before new ones are compiled and placed in `${INPUT_DIR}/backups`.

## Input Files
Each dotfile is compiled from its input file(s) to an output file of the corresponding name (e.g. a `gitconfig` file in the input directory  will be compiled to `.gitconfig` in the output directory (`$HOME` by   default)). Additionally, multiple input files can be compiled into a single dotfile using a naming scheme for input files.

That naming scheme is:

*xx-dotfile.ext_suffix*  
WHERE:  
*xx-* = input file priority (optional: the contents of highest-numbered input files will be placed in the output dotfile first, and other files matching *dotfile* will be inserted in lexographical order)  
*dotfile* = output dotfile name  
*.ext* = output dotfile extension (if applicable, e.g. tmux.conf)  
*_suffix* = input filename suffix (optional, ignored) 

Note: Any *.ext* occurring after an underscore ( _ ) will be considered part of the input file suffix and ignored.

For example: input files named `99-bashrc`, `98-bashrc_linux`, `bashrc_local.myaliases` will be compiled into a single `bashrc` output file (and in that order).

For further illustration, my input files can be found [here](https://github.com/rucker/dotfiles/tree/master/src).

## Example Use-Case
Your `.gitconfig` file is under version control and it contains your familiar global git configs. You want to clone the file from your git repository and use it on multiple machines where you use git. However, some machines require different configurations than others (such as the git identity being used). In addition, you want to easily be able to propagate any changes you make to your global `gitconfig` to all machines without manually copying and pasting anything.

What this script will allow you to do is automate management of all your git configurations across all machines, including local changes. This can be done by putting the common bits in a file called `gitconfig`, and the bits that vary from machine to machine in a second file, for example `gitconfig_local` as needed. Because Dotfiles Manager is able to infer the name of the dotfile being compiled from the names of the input files, the contents of `gitconfig` and `gitconfig_local` will be compiled into to a single `.gitconfig` file on each machine.

When you commit a new change to your global `gitconfig` in one place, you can keep everything up-to-date by doing a `git pull` to get your latest source files and then running `dfm.py ${INPUT_DIR}`.
