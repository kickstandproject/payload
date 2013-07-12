# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
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

"""
Various conveniences used for migration scripts
"""

import stripe.openstack.common.log as logging

LOG = logging.getLogger(__name__)


def create_tables(tables):
    for table in tables:
        LOG.info('Creating table %(table)s' % locals())
        table.create()


def drop_tables(tables):
    for table in tables:
        LOG.info('Dropping table %(table)s' % locals())
        table.drop()
