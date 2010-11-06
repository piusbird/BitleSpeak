## File: EspeakControler.py: BitleSpeak Client Driver for espeak
## Author: Matt Arnold <matt@thegnuguru.org> 
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


from subprocess import Popen, PIPE
import signal
from bitle.config import *
from bitle.util import *
_short_name = "Espeak"

def load_plugin(cfg):
    
  
    
    pa = cfg.getboolean(_short_name, "use_pulse")
    dbg = DEBUG
    spkr = EspeakPipe()
    spkr.set_parm("use_pulse", pa)
    spkr.set_parm("DEBUG", dbg)
    return spkr

class EspeakPipe(object):
     
    def __init__(self, *args):
         
        self.drvparm = {"DEBUG": DEBUG, "use_pulse": 1} ## lets make pulseaudio sane until i
        ## get configparser in place 6-28
        self.festival_proc = None ## rename later 7/20
        if not args:
            self.festival_args = [] ## do this so extend has no effect
        else:
            self.festival_args = args 
        self.paused = False
        self.running = False
    
    # Ok this will be weird but due to how this engine works we need some non-public  
    # methods for pipe control here before we can actually implement the interface
    
    def _running(self):
        
        return self.running
    def speak(self, text):
        
       # if self._running():  ## We don't permit multijobs in this driver
        #    print "fishy"
         #   return
        txt = str(text) ## execv is spiting up we want to know why
        p1 = Popen(['echo', txt], stdout=PIPE)
        fest_cmd = ['espeak']
        if self.drvparm["use_pulse"]:
            fest_cmd.insert(0, 'padsp')
        self.festival_proc = Popen(fest_cmd, stdin=p1.stdout)
        self.running = True
    
    def stop(self):
        
        if self._running():
            if self.drvparm["DEBUG"]:
                print "DEBUG: killing pipe"
            self.festival_proc.kill()
            self.running = False
    
    ## 8/8/10 Fix unreported issue with pause method
    def pause(self):
        
        if self._running(): 
            self.festival_proc.send_signal(signal.SIGSTOP)
            self.paused = True
            self.running = False
        elif self.paused:
            self.resume()
        else:
            return
        
    ## need to leave this in for pause to work
    def resume(self):
        
        if self.paused:
            
            self.festival_proc.send_signal(signal.SIGCONT)
            self.running = True

     
    def set_parm(self, key, val):
        
        self.drvparm[key] = val
    
    def get_parm(self, key):
    
        if key == None:
            
            return self.drvparm
        
        return self.drvparm[key]
