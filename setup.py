#!/usr/bin/env python

from setuptools import find_packages, setup

with open('VERSION.txt', 'r') as v:
    version = v.read().strip()

with open('requirements.txt', 'r') as reqs_file:
    reqs = reqs_file.read().splitlines()
    reqs = [r for r in reqs if r]

setup(
    name='fake-lock',
    version=version,
    packages=find_packages(exclude=['tests']),
    install_requires=reqs,
    license='MIT'
)
