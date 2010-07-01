#!/usr/bin/env python

## File bitlespeak.py: BitleSpeak Main program 
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
 
import sys
import os.path
try:  
    import pygtk  
    pygtk.require("2.0")  
except:  
    pass  
try:  
    import gtk  
except:  
    print("GTK Not Availible")
    sys.exit(1)

from bitle import loader
from bitle.config import *

spkr = None

try:
    spkr = loader.app_init()
except:
    print("Speech loader error")
    sys.exit(2)

class BitleSpeak(object):
    
    def __init__(self):
        
        ## see PyGtk Docs and data/ in source tree
        ui_file_path = os.path.abspath(BASE_PATH 
                                       + '/data/Bitletoolbar.ui')
        self.builder = gtk.Builder()
        self.builder.add_from_file(ui_file_path)
        dbg = self.builder.connect_signals(self)
        self.win = self.builder.get_object("mainWindow")
        self.win.show()
        if DEBUG:
            print "Unbound Events " + str(dbg)
        self.running = False  ## we don't want a seperate resume widget
        ## so this is used by play/stop widgets to determine behavior 
    
    def on_playButton_clicked(self, widget, data=None):
        """
        Speaks the clipboard contents when play is pressed
        """
        brd = gtk.clipboard_get()
        tts = brd.wait_for_text()
        spkr.speak(tts)
        self.running = True
        return
    
    def on_pauseButton_clicked(self, widget, data=None):
        
        if not self.running:
            spkr.pause()
        else:
            spkr.resume()
        return
    
    def on_stopButton_clicked(self, widget, data=None):
        
        if self.running:
            spkr.stop()
            self.running = False
        else:
            return
    
    def on_aboutButton_clicked(self, widget):
        
        about = gtk.AboutDialog()
        about.set_program_name(APP_NAME)
        about.set_authors([APP_AUTHOR])
        about.set_version(APP_VER)
        about.set_copyright("(c) 2010 Matt Arnold")
        about.set_comments(APP_DESC)
        about.run()
        about.destroy()
    
    def on_prefButton_clicked(self, widget, data=None):
        pass
    
    def on_mainWindow_destroy(self, widget, data=None):
        
        sys.exit(0)
    
    on_quitButton_clicked = on_mainWindow_destroy ## make gtk happy

if __name__ == '__main__':
    
    app = BitleSpeak()
    if DEBUG:
        print "GTK started"
    gtk.main()        
   
    
