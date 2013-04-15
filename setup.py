#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

with open('README.rst') as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    lines = requirements.readlines()
    libraries = [lib for lib in lines if not lib.startswith('-')]
    dependency_links = [link.split()[1] for link in lines if 
            link.startswith('-f')]

setup(
    name='oudjat',
    version='0.5',
    author='Adilla Susungi',
    author_email='adilla.susungi@etu.unistra.fr',
    maintainer='Arnaud Grausem',
    maintainer_email='arnaud.grausem@unistra.fr',
    url='http://repodipory.u-strasbg.fr/docs/oudjat',
    license='PSF',
    description='',
    long_description=long_description,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    download_url='http://repodipory.u-strasbg.fr/lib/python/',
    install_requires=libraries,
    dependency_links=dependency_links,
    keywords=['security', 'keywords'],
)
