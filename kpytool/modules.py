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
from os import path, mkdir, walk

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

        #this is the default module list
        self._moduleInfo = {
                                'name': '',
                                'parent': '',
                                'source': '',
                                'vcs': '',
                                'vcs-link': '',
                                'vcs-branch': '',
                                'build': '',
                                'install': '',
                                'build-system-options': ''
        }

        #this is the module name
        self._moduleName = moduleName

        self._moduleInfoList = []

        #this is the default module list
        self._moduleDefaultList = []


    @property
    def moduleName(self):
        return self._moduleName

    @moduleName.setter
    def moduleName(self, name):
        self._moduleName = name
        #now parse the data
        self._parseData()

    """
    Returns a list of dictionaries.
    Each dictionary represends a module..
    t['name']: module name, like kactivities
    t['parent']: parent name, like frameworks
    t['source']: source path
    t['vcs']: vcs type
    t['vcs-link']: the vcs link
    t['git-branch']: branch(only for git)
    t['build']: build dir
    t['install']: install dir
    t['build-system-options']: build system options
    """
    @property
    def moduleInfoList(self):
        return self._moduleInfoList

    @property
    def moduleDefaultList(self):
        return self._KpytoolCfg.default_modules

    """
    It will parse the config files
    """
    def _parseData(self):
        matches = []

        #initialize our reader
        reader = ConfigParser.RawConfigParser()

        if self.moduleName.find('/') == -1:
            pass
        else:
            logger.debug('starting dir for walk:\n' + path.join(self._KpytoolCfg.kpytool_configs, self.moduleName))
            #this is a meta module, like playground/base
            for root, dirnames, filenames in walk(path.join(self._KpytoolCfg.kpytool_configs, self.moduleName)):
                for filename in fnmatch.filter(filenames, '*.cfg'):
                    logger.debug('root:' + root)
                    logger.debug('dirnames:' + str(dirnames))
                    logger.debug('filename:' + filename + '\n')
                    reader.read(path.join(root, filename))
                    for moduleSection in reader.sections():
                        #print reader.sections()

                        #the frameworks.cfg contains 3 sections
                        #*kdelibs
                        #*kactivities
                        #*nepomuk-core
                        #iterate inside them
                        self._moduleInfo['name'] = reader.get(moduleSection, 'name')
                        self._moduleInfo['parent'] = root[len(self._KpytoolCfg.kpytool_configs) + len('/kpytool-configs/'):]

                        modulePath = reader.get(moduleSection, 'source-path')
                        self._moduleInfo['source'] = path.join(self._KpytoolCfg.kde_source, modulePath)

                        possibleVcs = ['git', 'svn', 'bzr']
                        for option in possibleVcs:
                            try:
                                self._moduleInfo['vcs-link'] = reader.get(moduleSection, option)
                                self._moduleInfo['vcs'] = option
                                try:
                                    #'git-branch' may not exist in a default *.cfg despite the fact that is git
                                    self._moduleInfo['git-branch'] = reader.get(moduleSection, 'git-branch')
                                except ConfigParser.NoOptionError:
                                    self._moduleInfo['git-branch'] = 'master'
                            except ConfigParser.NoOptionError:
                                pass

                        if not self._moduleInfo['vcs'] and not self._moduleInfo['vcs-link']:
                            #TODO fix this error
                            print 'errorrrrrrrrrrrrrrrrrr'


                        self._moduleInfo['build'] = path.join(self._KpytoolCfg.kde_build, modulePath)
                        self._moduleInfo['install'] = self._KpytoolCfg.kde_binaries

                        try:
                            self._moduleInfo['build-system-options'] = reader.get(moduleSection, 'build-system-options')
                        except ConfigParser.NoOptionError:
                            self._moduleInfo['build-system-options'] = self._KpytoolCfg.build_system_options


                        matches.append(self._moduleInfo)

        self._moduleInfoList = matches

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
        self._build_system_options = ''
        self._git_branch = ''
        self._default_modules = []
        self._kpytool_configs = ''

        #needed for _downloadKpytoolCfg
        self._kpytoolCfgPath = path

        self._cfgReader = ConfigParser.RawConfigParser()

        self._cfgReader.read(self._kpytoolCfgPath)

        self._read()

    def _read(self):
        self._kpytool_configs = path.join(self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kpytool-configs'))), 'kpytool-configs')
        self.kde_source = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kde-source')))
        self.kde_binaries = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kde-binaries')))
        self.kde_build = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kde-build')))
        self.kde_logs = self._verifyItem(path.expanduser(self._cfgReader.get('basic', 'kde-logs')))

        self.cmake_options = self._verifyItem(self._cfgReader.get('general', 'cmake-options'), False)
        self.git_branch = self._verifyItem(self._cfgReader.get('general', 'git-branch'), False)

        self.default_modules = self._verifyItem(self._cfgReader.get('basic', 'default-modules'), False).split(',')

        #download .kpytool.cfg
        self._downloadKpytoolCfg()

        #download the kpytool-configs tar and extract it
        self._downloadTarball()

    """
    Verify if the item is valid
    """
    def _verifyItem(self, item, createDirs = True):
        if item:
            if createDirs:
                if not path.exists(item) and not path.isdir(item):
                    mkdir(item)
            return item
        else:
            #TODO fix this error
            print 'Your .kpytool.cfg is damaged!!'
            return ''

    def _downloadKpytoolCfg(self):
        if not path.isfile(self._kpytoolCfgPath):
            u = urllib2.urlopen(KPYTOOL_CFG)
            with open(self._kpytoolCfgPath, 'w') as kpytool_cfg:
                kpytool_cfg.write(u.read())

            #its unlikely the code to reach here, but if it does, kpytool won't
            #work correctly so we have to be sure. For sure some other exception
            #would be raised but even in uber failure don't scary the user
            #TODO raise an exception here if the file doesn't exist

    def _downloadTarball(self):
        #now we need to check if the kpytool-config dir exists or not,
        #if it doesn't we will create it.
        if not path.exists(self._kpytool_configs) and not path.isdir(self._kpytool_configs):
            fileName = KPYTOOL_CONFIG_TARBALL.split('/')[-1]
            logger.debug('This is tarball\'s name ' + fileName)

            #download the tarball
            u = urllib2.urlopen(KPYTOOL_CONFIG_TARBALL)
            with open(fileName, 'wb') as file:
                file.write(u.read())
            with tarfile.open(fileName) as tar:
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
    def build_system_options(self):
        return self._build_system_options

    @build_system_options.setter
    def build_system_options(self, options):
        self._build_system_options = options

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