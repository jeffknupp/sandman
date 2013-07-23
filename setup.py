"""
"""
from __future__ import print_function
from setuptools import Command, setup

setup(
    name='Sandman',
    version='0.1-dev',
    url='http://github.com/jeffknupp/sandman/',
    license='BSD',
    author='Jeff Knupp',
    author_email='jeff@jeffknupp.com',
    description='Automated REST APIs for existing database-driven systems',
    long_description=__doc__,
    packages=['flask_sandman', 'flask_sandman.test'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    test_suite='sandman.test.suite'
)
