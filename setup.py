# -*- coding: utf-8 -*-
import os
import sys
import re

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'monkey', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

dependencies = [
    'khayyam',
    'pymqi',
    'pymlconf == 0.8.9'
]


setup(
    name="monkey",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    description="Scalable IBM Websphere MQ multi-thread scheduler.",
    packages=find_packages(),
    install_requires=dependencies,
    entry_points={
        'console_scripts': ['monkey = monkey:main']
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
