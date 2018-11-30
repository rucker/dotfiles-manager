# Dotfiles Manager
Dotfiles Manager allows for the compilation of dotfiles using a convention of [named input files](#input-files). A simple use-case might be:

`dfm.py ${INPUT_DIR}`

Where `${INPUT_DIR}` is the location of your input files.

See `dfm.py --help` for usage.

Existing dotfiles are backed up automatically before new ones are compiled and placed in `${INPUT_DIR}/backups`.

## Example Use-Case
You have a personal dotfiles repository containing your `.bashrc` and you want to use your familiar setup on multiple machines. You want to easily propagate any changes you make to your global `.bashrc` to all machines you use. However, some machines require different configurations (such as aliases, environment variables, or even sensitive data like access tokens, which you would not want to commit to your repo) than others. You want to keep your dotfiles repo in a clean state so you can easily `pull` global changes without losing track of those local changes you need (and without copying and pasting anything by hand). 

What Dotfiles Manager allows you to do is compile a single `.bashrc`file from separate source files: one containing your global configurations, and another containing the local (possibly sensitive) bits. This can be done by putting the common bits in a file called `bashrc` (which would be part of your dotfiles repo), and the bits that vary from machine to machine in a second file, for example called `bashrc_local` (which would be git-ignored). Because Dotfiles Manager is able to infer the name of the dotfile being compiled from the names of [input files](#input-files), the contents of `bashrc` and `bashrc_local` will be compiled into to a single `.bashrc` file on each machine.

When you push new `bashrc` changes to your dotfiles repo, you can keep everything up-to-date by doing a `git pull` to get your latest source files and then running `dfm.py ${INPUT_DIR}` to compile a `.bashrc` from the contents of your `bashrc` and `bashrc_local`.

## Input Files
### Symlinks
In simple cases where a single input file exists for a dotfile, a symlink to that file will be created. Otherwise, the output dotfile will be compiled from its source files.

### Dotfile Compilation
Each dotfile is compiled from its input files to an output file of the corresponding name (e.g. a `gitconfig` file in the input directory  will be compiled to `.gitconfig` in the output directory (`$HOME` by   default)). Additionally, multiple input files can be compiled into a single dotfile using a naming scheme for input files.

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
