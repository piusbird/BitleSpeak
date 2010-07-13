## File: util.py: Utility objects for bitle
## Author: Matt Arnold <matt@thegnuguru.org> 
## Start-Date: 7/9/10
## This file is part of BitleSpeak

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

import os

class BitleError(Exception):
    
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

class LoadError(BitleError):
    
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)


class SSIPError(BitleError):
    
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
                                    

def xsel_read():
    
    fp = os.popen('xsel')
    retval = fp.read()
    if retval == None:
        retval = "no text selected"
    return retval + '\n'
                                                           