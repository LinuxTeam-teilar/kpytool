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
import fnmatch
import ConfigParser
import tarfile
import urllib2
from os import path, mkdir

logger = logging.getLogger('kpytool.modules')
KPYTOOL_CONFIG_TARBALL = 'https://github.com/downloads/LinuxTeam-teilar/kpytool-configs/kpytool-configs-0.1.tar.gz'
KPYTOOL_CFG = 'https://github.com/downloads/LinuxTeam-teilar/kpytool-configs/kpytool.cfg'

"""
This class will retrieve the informations for each module
"""
class ModuleReader(object):
    def __init__(self, kpytoolConfig, moduleName = ''):
        #initialize the config reader for .kpytool.cfg
        self. _KpytoolCfg =  _KpytoolConfigReader(kpytoolConfig)

        #take the info
        self._KpytoolCfg.read()

        #this is the default module list
        self._moduleDefaultList = []

        #this is the module name
        self._moduleName = moduleName

        self._moduleInfo = '' , '', '', ('', ''), '', '', ''


    @property
    def moduleName(self):
        return self._moduleName

    @moduleName.setter
    def moduleName(self, name):
        self._moduleName = name
        #now parse the data
        self._parseData()

    """
    returns a tuple which represends a module.
    For instance frameworks contains kdelibs and kactivities.
    So we will have 2 tuples and each of it will have
    t[0]: module name, like kactivities
    t[1]: parent name, like frameworks
    t[2]: source path
    t[3]: vcs, the link and branch(only for git)
    t[4]: build dir
    t[5]: install dir
    t[6]: build system args
    """
    @property
    def moduleInfo(self):
        return self._moduleInfo

    @moduleInfo.setter
    def moduleInfo(self, info):
       self._moduleInfo = info

    @property
    def moduleDefaultList(self):
        #for i in self. _KpytoolCfg.default_modules:
        #     self.moduleName = i
        #    self._moduleList.append(self.moduleInfo)
        return self._moduleDefaultList

    #TODO avoid setter, we want this to be
    #just read-only
    #@moduleList.setter
    #def moduleList(self, list):
    #    self._moduleList = list

    """
    It will parse the config files and it will return a boolean.
    This method should be called before moduleList
    """
    def _parseData(self):
        self.moduleName #Do something
        ok = False
        matches = []
        for root, dirnames, filenames in os.walk(self._KpytoolCfg.kpytool_configs):
            for filename in fnmatch.filter(filenames, '*.cfg'):
                #matches.append(os.path.join(root, filename))
                logger.debug('root:' + root)
                logger.debug('dirnames:' + str(dirnames))
                logger.debug('filename:' + filename + '\n')
                #TODO add more

        return ok

"""
This class will retrieve the information
from the .kpytool.cfg file
"""
class _KpytoolConfigReader(object):
    def __init__(self, path):
        self._kde_source = ''
        self._kde_binaries = ''
        self._kde_build = ''
        self._kde_logs = ''
        self._cmake_options = ''
        self._git_branch = ''
        self._default_modules = []
        self._kpytool_configs = ''

        #needed for _downloadKpytoolCfg
        self._kpytoolCfgPath = path


        #download .kpytool.cfg
        self._downloadKpytoolCfg()

        self._cfgReader = ConfigParser.RawConfigParser()

        self._cfgReader.read(self._kpytoolCfgPath)


    def read(self):
        self.kpytool_configs = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kpytool-configs')))
        self.kde_source = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kde-source')))
        self.kde_binaries = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kde-binaries')))
        self.kde_build = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kde-build')))
        self.kde_logs = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kde-logs')))

        #we need to check if the above dirs exist or not, if they don't then we will create them
        self._verifyDirs()

        self.cmake_options = self._verifyItem(self._cfgReader.get('general', 'cmake-options'))
        self.git_branch = self._verifyItem(self._cfgReader.get('general', 'git-branch'))

        self.default_modules = self._verifyItem(self._cfgReader.get('general', 'default-modules')).split(',')

    def _downloadKpytoolCfg(self):
        if not path.isfile(self._kpytoolCfgPath):
            u = urllib2.urlopen(KPYTOOL_CFG)
            with open(self._kpytoolCfgPath, 'w') as kpytool_cfg:
                kpytool_cfg.write(u.read())

            #its unlikely the code to reach here, but if it does, kpytool won't
            #work correctly so we have to be sure. For sure some other exception
            #would be raised but even in uber failure don't scary the user
            #TODO raise an exception here if the file doesn't exist

    """
    Verify if the item is valid
    """
    def _verifyItem(self, item):
        if item:
            return item
        else:
            print 'Your .kpytool.cfg is damaged!!'
            return ''

    def _verifyDirs(self):
        #first check for the more 'common' dirs
        for d in [self.kde_source, self.kde_binaries, self.kde_build, self.kde_logs]:
            if not path.exists(d) and not path.isdir(d):
                mkdir(d)

        #now we need to check if the kpytool-config dir exists or not,
        #if it doesn't we will create it.
        if not path.exists(self.kpytool_configs) and not path.isdir(self.kpytool_configs):
            fileName = KPYTOOL_CONFIG_TARBALL.split('/')[-1]
            logger.debug('This is tarball\'s name ' + fileName)

            #download the tarball
            u = urllib2.urlopen(KPYTOOL_CONFIG_TARBALL)
            with open(fileName, 'wb') as tar:
                tar.write(u.read())

                #extract the tarball
                tar.extractall(self.kpytool_configs)

            #its unlikely the code to reach here, but if it does, kpytool won't
            #work correctly so we have to be sure. For sure some other exception
            #would be raised but even in uber failure don't scary the user
            #TODO raise an exception here if the dirs doesn't exist



    @property
    def kde_source(self):
        return self._kde_source

    @kde_source.setter
    def kde_source(self, source):
        self._kde_source = source

    @property
    def kde_binaries(self):
        return self._kde_binaries

    @kde_binaries.setter
    def kde_binaries(self, path):
        self._kde_binaries = path

    @property
    def kde_logs(self):
        return self._kde_logs

    @kde_logs.setter
    def kde_logs(self, path):
        self._kde_logs = path

    @property
    def kde_build(self):
        return self._kde_build

    @kde_build.setter
    def kde_build(self, path):
        self._kde_build = path

    @property
    def cmake_options(self):
        return self._cmake_options

    @cmake_options.setter
    def cmake_options(self, path):
        self._cmake_options = path

    @property
    def git_branch(self):
        return self._git_branch

    @git_branch.setter
    def git_branch(self, path):
        self._git_branch = path

    @property
    def default_modules(self):
        return self._default_modules

    @default_modules.setter
    def default_modules(self, path):
        self._default_modules = path

    @property
    def kpytool_configs(self):
        return self._kpytool_configs

    @kpytool_configs.setter
    def kpytool_configs(self, path):
        self._kpytool_configs = path