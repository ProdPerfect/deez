#!/usr/bin/env python3
# type: ignore
from setuptools import find_packages, setup

from deez.__version__ import __author__, __email__, __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='deez',
      version=__version__,
      description='A little library to simplify building small APIs on top of API Gateway and Lambda.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=__author__,
      author_email=__email__,
      packages=find_packages(exclude=["tests"]),
      url='https://github.com/prodperfect/deez',
      include_package_data=True,
      package_data={
          '': ['*.pyi'],
      },
      zip_safe=True,
      license='MIT',
      python_requires='>=3.6',
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ])
