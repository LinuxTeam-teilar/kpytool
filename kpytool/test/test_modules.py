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

import modules
