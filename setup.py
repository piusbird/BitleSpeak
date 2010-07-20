#!/usr/bin/env python

## File: setup.py: If you don't know what this file does see pydoc
## marnold 7/20/10

## Copyright (c) 2010 Matt Arnold
## BitleSpeak is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## BitleSpeak is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with BitleSpeak.  If not, see <http://www.gnu.org/licenses/>.

## side note I'm getting kinda tired of pasting these copyright headers
## but Debian's FTPmasters will seeing this shortly so on best behavior

from distutils.core import setup
from bitle.config import *

setup(name='BitleSpeak',
      version = APP_VER,
      description = APP_DESC,
      author = 'Matt Arnold',
      author_email = 'mattarnold5@gmail.com',
      license = 'GPLv3',
      url = 'http://marnold.info/code/bitlespeak',
      packages = ['bitle'],
      scripts = ['bitlespeak'],
      data_files = [('share/bitlespeak', ['data/Bitletoolbar.ui', 
      				'data/bitlespeak.xpm']),
                     ('share/doc/bitlespeak', ['docs/bitle.dist.cf', 
                     'docs/bitle.dev.cf', 
                     'docs/plugin-interface.txt'])
                   ]
     
	    
)

      
      

