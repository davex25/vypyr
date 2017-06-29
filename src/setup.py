#!/usr/bin/python2
from setuptools import setup

setup(name="vypyr",
        version="0.1",
        description="vypyr controller",
        url='http://github.com/davex25/vypyr',
        author="David Friberg",
        author_email="dfriberg23@gmail.com",
        license="MIT",
        packages=['vypyr'],
        install_requires=[
            'mido'
            ],
        zip_safe=False)

