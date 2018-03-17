#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

__author__ = 'Etti Horada <etti@gmail.com>'
__date__ = 'March 17, 2018'

from setuptools import setup

VERSION = '0.1'

ME = 'University of Haifa'
MY_MAIL = 'etti@gmail.com'
PACKAGE_NAME = 'ieee_parser'
URL = ""
DESCRIPTION = "..."
LONG_DESCRIPTION = open('README.md').read()
REQUIREMENTS = open('requirements.txt').readlines()
SUB_MODULES = ['ieee_parser']


def do_setup():
    setup(name=PACKAGE_NAME,
          version=VERSION,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          author_email=MY_MAIL,
          author=ME,
          url=URL,
          platforms=['linux'],
          packages=SUB_MODULES,
          classifier=['Private :: Do Not Upload'],  # hack to avoid uploading to pypi
          install_requires=REQUIREMENTS,
          scripts=['bin/ieee.py'],
          # entry_points = {
          #     'console_scripts': [
          #         'command-name = ieee_parser.collect:main',
          #     ],
          # },
          )


def main():
    do_setup()

if __name__ == '__main__':
    main()
