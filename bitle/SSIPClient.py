## File: SSIPClient.py: A client class for Speech Synthesis 
## Interface Protocol. Note there is a higher level python interface
## but given that Freebsoft's Speech Dispatcher has been forked
## I don't want to use one API over the other for fear of 
## libary incompatiblites between the two projects.
## so I get to reinvent the wheel. Boy programing is fun

## Author: Matt Arnold <matt@thegnuguru.org>
## Reminder to people modifying this
## Myself included 
## READ THE SPEC at http://tinyurl.com/SSIP-Docs
## failure to read the spec will get all patches
## sent to /dev/null got it good

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

## Note: 6-20-10 SSIP template strings 
## should proably be somewhere else in-case there are
## protocol changes  
## Note: 6-28-10: DocString m7560e please kthanks bye

from socket import *
import os
from bitle.config import *

MAGIC_HOST = "UNIX" ## argument that passes to the consturctor to enable bsd
## socket support AF_UNIX

_short_name = "SSIPClient"

def load_plugin(cfg):
	
	host = cfg.get(_short_name, 'host')
	port = cfg.get(_short_name, 'port')
	if port.isdigit() and port == '-1':
		port = int(os.environ["SPEECHD_PORT"])	
	
        if host != MAGIC_HOST:
            port = int(port)

	if DEBUG:
		print "SSIPClient loading"
		print "server: " + host
		print "port " +  str(port)
		
	spkr = SSIPClient(host, port)
	ubu = cfg.getboolean(_short_name, "ubuntu")
	voice = cfg.get(_short_name, "voice")
	if spkr.set_voice(voice) and DEBUG:
		
		print "Voice set"
	elif DEBUG:
		
		print "voice not set"
	
	else: 
		pass
	spkr.set_parm('ubuntu', ubu)
	return spkr 



class SSIPClient(object):

	def __init__(self, host, port):
		
                addr_fam = AF_INET
                
                if host == MAGIC_HOST:
                    
                    addr_fam = AF_UNIX

                self.skt = socket(addr_fam, SOCK_STREAM) 
		self.drvparm = {"DEBUG": 0, "ubuntu": 0}
		if DEBUG:
			
			self.drvparm["DEBUG"] = 1
			
		self.currjob = -1
		if host == MAGIC_HOST:
                    
                    self.skt.connect(port)
                else:
                    
                    self.skt.connect((host, port))
		
                if self.drvparm["DEBUG"]:
			print "DEBUG: shandler connected doing handshake"
		smsg = "SET self CLIENT_NAME " + str(os.getlogin()) 
		smsg += CLIENT_NAME + LINE_ENDING
		if self.drvparm["DEBUG"]:
			print "DEBUG: User Agent " + smsg
		self.skt.send(smsg)
		rmsg = self.skt.recv(BUFFSIZE)
		if rmsg[0] != OK_STATE:
			raise SSIPError(rmsg)
	
	## Section 4.2
	def speak(self, text):
		
		msg = str(text) + LINE_ENDING + '.' + LINE_ENDING
		self.skt.send("SPEAK\r\n")
		rmsg = self.skt.recv(BUFFSIZE)
		if rmsg[0] != OK_STATE:
			
			raise SSIPError(rmsg)
		else:
			self.skt.send(msg)
			rmsg = self.skt.recv(BUFFSIZE)
			i = rmsg.index('\r') ## this is the point at which we 
			## get less useful information
			self.currjob = int(rmsg[4:i])
	
	def pause(self):
		
		## Ugly hack for LP: #596703 
		if self.drvparm["ubuntu"]:
			
			self.stop()
			return
		
		smsg = "PAUSE " + str(self.currjob) + LINE_ENDING
		self.skt.send(smsg)
		rmsg = self.skt.recv(BUFFSIZE)
		if self.drvparm["DEBUG"]:
			
			print "Sent: " + smsg
			print "Got: " + rmsg
		if rmsg[0] != OK_STATE:
			
			raise SSIPError(rmsg)
			
		else:
			
			return
	
				
	def get_currjob(self):
	
		return int(self.currjob)
	
	def stop(self):
		
		smsg = "CANCEL self" + LINE_ENDING 
		## also stops currently queued jobs
		self.skt.send(smsg)
		rmsg = self.skt.recv(BUFFSIZE)
		if self.drvparm["DEBUG"]:
			
			print "Sent: " + smsg
			print "Got: " + rmsg
		if rmsg[0] != OK_STATE:
			
			raise SSIPError(rmsg)
			
		else:
			
			return
	
	def resume(self):
		
		if self.drvparm["ubuntu"]:
			return
		
		smsg = "RESUME " + str(self.currjob) + LINE_ENDING
		self.skt.send(smsg)
		rmsg = self.skt.recv(BUFFSIZE)
		
		if self.drvparm["DEBUG"]:
			
			print "Sent: " + smsg
			print "Got: " + rmsg
		if rmsg[0] != OK_STATE:
			
			raise SSIPError(rmsg)
			
		else:
			
			return
	
	def set_parm(self, key, val):
		
		self.drvparm[key] = val
	
	def get_parm(self, key):
	
		if key == None:
			
			return self.drvparm
		
		return self.drvparm[key]
	
	def set_voice(self, voice):
		
		smsg = "SET self VOICE " + voice + LINE_ENDING 
		self.skt.send(smsg)
		rmsg = self.skt.recv(BUFFSIZE)
		if rmsg[0] != OK_STATE:
			
			return 0
		else:
			return -1
	
	def __del__(self):
		
		smsg = "QUIT" + LINE_ENDING
		self.skt.send(smsg)
		self.skt.close()

