#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for trainwarner"""

from setuptools import setup, find_packages
import os

version = "0.1.0"
here = os.path.abspath(os.path.dirname(__file__))

with open(
    os.path.join(here, 'README.rst'), 'r', encoding='utf-8'
) as readme_file:
    readme = readme_file.read()

with open(
    os.path.join(here, 'CHANGELOG.rst'), 'r', encoding='utf-8'
) as changelog_file:
    changelog = changelog_file.read()

requirements = [
    'cryptography',
    'sqlalchemy',
    'anyblok',
    'psycopg2-binary',
    'marshmallow-sqlalchemy<=0.17.0',
    'anyblok_marshmallow',
    'anyblok_pyramid',
    'pyramid_jinja2',
    'anyblok_pyramid_beaker',
    'anyblok_pyramid_rest_api',
    'cornice_swagger',
    'requests',
    'gunicorn',
    'Faker',
    'Babel',
    'anyblok_mixins',
    'anyblok_postgres'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='trainwarner',
    version=version,
    description="TrainWarner project designed for setuping watchdogs on train journeys",
    long_description=readme + '\n\n' + changelog,
    author="Alexis Tourneux",
    author_email='tourneuxalexis@gmail.com',
    url='https://github.com/AlexTorx/trainwarner',
    packages=find_packages(),
    entry_points={
        'bloks': [
            'trainwarner=trainwarner_project.bloks.trainwarner:Trainwarner'
            ],
        'console_scripts': [
            'anyblok_populate_stations='
            'trainwarner_project.bloks.trainwarner.scripts:populate_stations',
            'anyblok_populate_reduction_cards='
            'trainwarner_project.bloks.trainwarner.scripts'
            ':populate_reduction_cards'
            ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='trainwarner',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
