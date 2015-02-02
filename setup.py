#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.rst'
    )
).read()

setup(
    name='pydocverter',
    version='0.0.0',
    url='https://github.com/msabramo/pydocverter',
    license='MIT',
    description='Client for Docverter document conversion service',
    long_description=long_description,
    author='Marc Abramowitz',
    author_email='marc@marc-abramowitz.com',
    py_modules=['docverter'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
    ],
)
