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
    author='Austin Jackson',
    author_email='austinjackson892@gmail.com',
    entry_points={
        'console_scripts': [
            'histstat = histstat.histstat:main',
        ]
    },
    install_requires=['psutil']
)
