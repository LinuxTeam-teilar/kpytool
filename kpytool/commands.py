#  Copyright 2012 by Giorgos Tsiapaliokas <terietor@gmail.com>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; see the file COPYING.  If not, write to
#  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.

import logging
from os import path

logger = logging.getLogger('kpytool.commands')

class Commands(object):
    def __init__(self, moduleName, moduleParent):
        #TODO fix this brain dead line!!!
        print "Preparing " + moduleName + "from " + moduleParent


    def src(self, source_path):
        #check if we have a svn or git or bzr repo
        if path.exists(path.join(source_path + '.git')):
            #Do some git stuff
        elif path.exists(path.join(source_path + '.svn')):
            #Do some svn stuff
        elif path.exists(path.join(source_path + '.bzr')):
            #Do some bzr stuff

    def configure(self, source_path, build_path):
        if path.exists(path.join(source_path + 'CMakeLists.txt')):
            #Do some cmake stuff
        elif if path.exists(path.join(source_path + '*.pro')):
            #Do some autotools stuff
        elif if path.exists(path.join(source_path + 'makefile.am')):
            #Do bla bla

    def build(self, build_path):
        #build the project

    def install(self, build_path):
        #install the project



