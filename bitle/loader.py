## File: loader.py: BitleSpeak backend loader 
## A sane way of loading configuration data and 
## Speaker plugins
## Matt Arnold <matt@thegnuguru.org> 6-30-10
##
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

import ConfigParser 
import os, os.path
from sys import exit
from bitle.config import *
from bitle.util import *


cfg = ConfigParser.ConfigParser()

def app_init(cfg_path = None):
    
    d_cfg = os.path.abspath(BASE_PATH + '/bitle.cf')
    s_cfg = os.path.abspath(SITE_CONFIG_DIR + '/bitle.cf')
    u_cfg = os.path.expanduser('~/.bitle.cf')
    if cfg_path is not None and os.path.exists(cfg_path):
        cfg.read(cfg_path)
    # load developer config first
    elif os.path.exists(d_cfg):
        cfg.read(d_cfg)
    elif os.path.exists(u_cfg):
        cfg.read(u_cfg)
    elif os.path.exists(s_cfg):
        cfg.read(s_cfg)
    else:
        raise LoadError("Failed to load config file")
    
    plugin = cfg.get("global", "speech_plugin")
    if DEBUG:
        print plugin[0:5]
    
    if plugin[0:5] != 'bitle': ## security check
        ## if we are not in the right package BREAK OUT NOW
        print "Security Check failed"
        exit(2)
    strexec = "from " + plugin + " import load_plugin" 
    ## yet more security if we don't have a load_plugin this will fail
    ## on a pile of uncaught exceptions. i still need to figure out some 
    ## way of plugin signing 
    exec(strexec)
    if load_plugin:
        spkr = load_plugin(cfg)
        return (spkr, cfg) 
    else:
        raise LoadError("invalid plugin")  
    return 


    
