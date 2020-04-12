#!/usr/bin/env python

from setuptools import setup

setup(
    name='histstat',
    packages=['histstat'],
    version='1.1.5',
    description='History for netstat.',
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