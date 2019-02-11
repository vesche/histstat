#!/usr/bin/env python

import histstat
from setuptools import setup

setup(
    name='histstat',
    packages=['histstat'],
    version=histstat.__version__,
    description='History for netstat.',
    license='MIT',
    url='https://github.com/vesche/histstat',
    author=histstat.__author__,
    author_email=histstat.__email__,
    entry_points={
        'console_scripts': [
            'histstat = histstat.histstat:main',
        ]
    },
    install_requires=['psutil'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Security"
    ]
)