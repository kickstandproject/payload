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

from pecan import rest
from wsmeext import pecan as wsme_pecan

from stripe.common import schema
from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class SchemasController(rest.RestController):
    """REST Controller for Schemas."""

    _custom_actions = {
        'member': ['GET'],
        'queue': ['GET'],
    }

    @wsme_pecan.wsexpose(unicode)
    def member(self):
        """Retrieve schema for a member."""
        json = {
            'id': {
                'type': 'integer',
            },
            'created_at': {
                'type': ['string', 'null'],
            },
            'description': {
                'type': ['string', 'null'],
            },
            'disabled': {
                'type': 'boolean',
            },
            'name': {
                'type': 'string',
            },
            'password': {
                'type': 'string',
            },
            'updated_at': {
                'type': ['string', 'null'],
            },
        }

        return schema.Schema('member', json).raw()

    @wsme_pecan.wsexpose(unicode)
    def queue(self):
        """Retrieve schema for a queue."""
        json = {
            'id': {
                'type': 'integer',
            },
            'created_at': {
                'type': ['string', 'null'],
            },
            'description': {
                'type': ['string', 'null'],
            },
            'disabled': {
                'type': 'boolean',
            },
            'name': {
                'type': 'string',
            },
            'updated_at': {
                'type': ['string', 'null'],
            },
        }

        return schema.Schema('queue', json).raw()
