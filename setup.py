#!/usr/bin/env python

from distutils2.core import setup

setup(name='kpytool',
      version = '0.1',
      summary = 'install KDE from sources',
      author = 'Giorgos Tsiapaliokas',
      author_email= 'terietor@gmail.com',
      maintainer = 'Giorgos Tsiapaliokas',
      maintainer_email= 'terietor@gmail.com',
      home_page = 'https://github.com/LinuxTeam-teilar/kpytool',
      license = 'GPLv2',
      scripts = [kpytool/kpytool]
      packages = ['kpytool']
)