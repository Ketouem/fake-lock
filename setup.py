#!/usr/bin/env python

from setuptools import find_packages, setup

with open('requirements.txt', 'r') as reqs_file:
    reqs = reqs_file.read().splitlines()
    reqs = [r for r in reqs if r]

setup(
    name='fake-lock',
    version='0.1-dev',
    packages=find_packages(),
    install_requires=reqs
)
