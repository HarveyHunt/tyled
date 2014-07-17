#!/usr/bin/python3
import os
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='tyled',
      packages=find_packages(),
      version='0.0.1',
      description='A lightweight image tiler written in Python.',
      author='Harvey Hunt',
      url='https://github.com/HarveyHunt/tyled',
      author_email='harveyhuntnexus@gmail.com',
      license="GPLv3",
      keywords="python3 tyled pillow pil images tiling wallpaper tiled",
      install_requires=['pillow'],
      long_description=read('README.md'),
      entry_points={'console_scripts': ['tyled=tyled.tyled:init']})
