#!/usr/bin/env python
from setuptools import setup, find_packages
from sys import version_info
from cronbeat.version import VERSION

requirements = ['opbeat']
if version_info < (2, 7, 0):
    requirements.append('argparse')

setup(
    name='cronbeat',
    version=VERSION,
    author='Peter Naudus',
    author_email='uselinux@gmail.com',
    description='CronBeat is a command-line wrapper that reports unsuccessful runs to OpBeat (https://www.opbeat.com)',
    long_description=open('README.md').read(),
    license='MIT',
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    url='http://github.com/linuxlefty/CronBeat',
    packages=find_packages(),
    install_requires=requirements,
    data_files=[],
    entry_points={
        'console_scripts': [
            'cronbeat = cronbeat.runner:run',
        ]
    }
)
