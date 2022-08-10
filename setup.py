#!/usr/cli/env python

from distutils.core import setup
import supportbot

setup(
      name='NYCMeshSupportBot',
      version=supportbot.__version__,
      description='Support Chatbot for NYC Mesh',
      author='Andy Baumgar & Andrew Dickinson',
      author_email='support@nycmesh.net',
      url='https://nycmesh.net/',
      packages=['supportbot'],
      entry_points={
            'console_scripts': ['supportbot-server=supportbot.cli.bot_server:main'],
      }
)

