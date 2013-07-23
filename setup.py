"""
"""
from __future__ import print_function
from setuptools import Command, setup

setup(
    name='Sandman',
    version='0.1-dev',
    url='http://github.com/jeffknupp/sandman/',
    license='Apache',
    author='Jeff Knupp',
    author_email='jeff@jeffknupp.com',
    description='Automated REST APIs for existing database-driven systems',
    long_description=__doc__,
    packages=['sandman', 'sandman.test'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    test_suite='sandman.test.test_sandman',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
 
)
