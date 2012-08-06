#!/usr/bin/env python

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

import argparse
import logging
from modules import ModuleReader
from os import getcwd, environ, path

def main():
    parser = argparse.ArgumentParser('A tool which helps you to build KDE from sources')

    parser.add_argument('--only-src', action = 'store_true',
                        default = False, dest = 'src',
                        help = 'Update the module, don\'t do anything else')

    parser.add_argument('--no-src', action = 'store_true',
                        default = False, dest = 'no_src',
                        help = 'Don\'t update the module, but build it, configure it and install it')

    parser.add_argument('--only-configure', action = 'store_true',
                        default = False, dest = 'configure',
                        help = 'Just configure the module, don\'t do anything else')

    parser.add_argument('--only-build', action = 'store_true',
                        default = False, dest = 'build',
                        help = 'Just build the module, don\'t do anything else')


    parser.add_argument('--only-install', action = 'store_true',
                        default = False, dest = 'install',
                        help = 'Just install the module, don\'t do anything else')

    configDefault = path.join(environ['HOME'], '.kpytool.cfg')
    parser.add_argument('--config', action = 'store',
                        default = configDefault, dest = 'config',
                        help = 'Specify a new path for the kpytool config, the default is ~/.kpytool.cfg')

    parser.add_argument('--debug', action = 'store_true',
                        default = False, dest = 'debug',
                        help = 'Use it in order to have a debug output')

    #take the results and the modules
    tmp = parser.parse_known_args()
    results = tmp[0]
    modules = tmp[1]

    #create our logger
    logger = logging.getLogger('kpytool')

    if results.debug:
        logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug('This is namespace of argparse:\n' + str(results) + '\n')

    logger.debug('These are the modules:\n' + str(modules) + '\n')

    logger.debug('The kpytool config is:' + results.config)

    m = ModuleReader('kdelibs')
    m.parseData()
    if not results.src and \
    not results.configure and \
    not results.build and \
    not results.install:
        #the user has used ./kpytool $someModule, so
        #pretend that the above are correct!
        #and update, configure, build and install
        pass

    elif results.src:
        #dl
        pass

    elif results.no_src:
        #dl, configure, build and install
        pass

    elif results.configure:
        #configure
        pass

    elif results.build:
        #build
        pass

    elif results.install:
        #install
        pass


if __name__ == '__main__':
    main()