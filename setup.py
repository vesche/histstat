#!/usr/bin/env python

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='histstat',
    packages=['histstat'],
    version='1.2.0',
    description='History for netstat.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/vesche/histstat',
    author='Austin Jackson',
    author_email='vesche@protonmail.com',
    entry_points={
        'console_scripts': [
            'histstat = histstat.histstat:main',
        ]
    },
    install_requires=['psutil'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Security'
    ]
)