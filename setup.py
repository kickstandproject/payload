# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Author: Paul Belanger <paul.belanger@polybeacon.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.

import setuptools

from stripe.openstack.common import setup
from stripe.version import VERSION_INFO as version


requires = setup.parse_requirements()
test_requires = setup.parse_requirements(['tools/test-requires'])
depend_links = setup.parse_dependency_links()

setuptools.setup(
    name='stripe',
    version=version.canonical_version_string(always=True),
    author='Paul Belanger',
    author_email='paul.belanger@polybeacon.com',
    url='https://github.com/kickstandproject/stripe',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=setup.get_cmdclass(),
    install_requires=requires,
    setup_requires=['setuptools_git>=0.4'],
    dependency_links=depend_links,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'stripe-api=stripe.cmd.api:main',
        ],
    }
)
