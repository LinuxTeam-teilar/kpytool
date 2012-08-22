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

"""
modules.py does the above,
* download the tarball 'kpytool-configs' and the file '.kpytool.cfg'
This is automatically checked inside the kpytool, if the above doesn't
exist an exception will be raised
* check if the below dirs exist and if they valid according to the ones from the .kpytool.cfg
    **kpytool-configs
    **kde-source
    **kde-binaries
    **kde-logs
    **kde-build
*check if the default_modules list matches the one given
from the kpytool.cfg file
*check if ModuleReader.moduleInfo property returns valid data
"""

from modules import ModuleReader
from os import path, environ
import logging

logger = logging.getLogger('test_kpytool.test_modules')

MODULE_NAME = 'kactivities'

def do():

    #initialize
    p = path.join(environ['HOME'], '.kpytool.cfg')
    logger.debug(p)
    reader = ModuleReader(MODULE_NAME, p)

    reader.moduleName = MODULE_NAME

    #check module info
    logger.debug('module name' + reader.moduleInfo[0])
    logger.debug('parent path' + reader.moduleInfo[1])

    _checkPath('source path', reader.moduleInfo[2])

    for vcs, link, branch in reader.moduleInfo[3]:
        logger.debug('vcs:' + vcs)
        logger.debug('link:' + link)
        logger.debug('branch:' + branch)

    _checkPath('build path', reader.moduleInfo[4])
    _checkPath('install path', reader.moduleInfo[5])

    logger.debug('build system args' + reader.moduleInfo[6])

    #check default modules
    l = [
        'automoc',
        'cagibi',
        'akonadi'
    ]
    if len(returnsMatches(reader.moduleList, l)) != 3:
        logger.debug('the default list modules aren\'t correct')

def _checkPath(pathName, path):
    if not path.exists(path) and not path.isdir(path):
        logger.debug(path + 'doesn\'t exist!!!!!')
    else:
        logger.debug(pathName + path)