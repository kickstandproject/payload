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

from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class QueueCallersController(rest.RestController):
    """REST Controller for queue callers."""

    @wsme_pecan.wsexpose(None, unicode)
    def get_all(self, queue_id):
        """Retrieve a list of queue callers."""

        # TODO(pabelanger): Implement redis backend for queue callers.
        res = {
            'id': 1,
            'created_at': None,
            'name': 'John Doe',
            'number': '6135551234',
            'position': 1,
            'queue_id': queue_id,
            'updated_at': None,
        }

        return res
