#!/usr/bin/env python

import os
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.core import setup


class CustomInstall(install):
    """This custom install command will build and install native agent_lib using it's makefile"""

    def run(self):
        os.chdir('./acpc_python_client/agent_lib')
        os.system('make')
        os.chdir('../../')
        install.run(self)


class CustomClean(clean):
    """This custom clean command will clean temporary files
    from build including files from native agent_lib using it's makefile"""

    def run(self):
        os.chdir('./acpc_python_client/agent_lib')
        os.system('make clean')
        os.chdir('../../')
        clean.run(self)


setup(name='acpc_python_client',
      version='1.0',
      author='Jakub Petriska',
      packages=[
          'acpc_python_client',
          'acpc_python_client.agent_lib',
          'acpc_python_client.data'
      ],
      package_dir={'acpc_python_client.agent_lib': 'acpc_python_client/agent_lib'},
      package_data={
          'acpc_python_client.agent_lib': ['libplayer.so']
      },
      cmdclass={
          'install': CustomInstall,
          'clean': CustomClean
      })
