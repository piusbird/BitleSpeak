## Bitlespeak static defines 
## Matt Arnold 6/1/10
## Copyright (c) Matt Arnold
## Some rights reserved
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



LINE_ENDING = '\r\n'
BUFFSIZE = 2048 ## expecting 2^10 bytes lets double that
OK_STATE = '2' ## see spec
DEBUG = 1
CLIENT_NAME = ":bittlespeak:shandler"
BASE_PATH = '.'
SITE_CONFIG_DIR = '/etc'


## GTK author metadata

APP_NAME = 'BitleSpeak'
APP_VER = '0.1.1b2'
APP_AUTHORS = ["Matt Arnold"]
APP_COPY ='GPL'
APP_DESC = 'A little text to speech toolbar'

## UI stuff
PREF_MSG = "Plese edit bitle.cf for application settings"