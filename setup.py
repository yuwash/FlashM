#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from flashm import __version__

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'prompt_toolkit>=2.0',  # not yet available from PyPI
    # please use Pipfile to install it from git
]

setup_requirements = [
]

# test_requirements = [
# ]

setup(
    name='FlashM',
    version=__version__,
    description="A still simple cli flash card application compatible "
    "with lesson files of Pauker",
    long_description=readme + '\n\n' + history,
    author="Yushin Washio",
    author_email='yuwash at yandex dot com',
    url='https://github.com/yuwash/FlashM',
    packages=find_packages(include=['flashm']),
    entry_points={
        'console_scripts': [
            'flashm = flashm.__main__:main',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license='GNU General Public License v3',
    zip_safe=False,
    keywords=[
        'flashcards',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        # uncomment when tested
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
    # test_suite='tests',
    # tests_require=test_requirements,
    setup_requires=setup_requirements,
)
