#!/usr/bin/env python3
from setuptools import setup

from deez import __author__, __email__, __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='deez',
      version=__version__,
      description='A little library I building to simplify building small web services (mostly APIs) on top of AWS Lambda.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=__author__,
      author_email=__email__,
      packages=['deez', 'deez.conf'],
      url='https://github.com/rhymiz/yamz',
      include_package_data=True,
      zip_safe=False,
      license='MIT',
      python_requires='>=3.5',
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ])