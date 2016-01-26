#!/usr/bin/python

from distutils.core import setup

setup(name = 'dotfiles',
      version = '2.1',
      description = 'A dotfile compilation/setup utility.',
      author = 'Rick Ucker',
      url = 'https://github.com/rucker/dotfiles',
      license = 'MIT',
      packages = ['dotfiles','test'],
      requires = ['mock','enum34'],
     )
