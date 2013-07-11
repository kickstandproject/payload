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

import pecan
import wsmeext.pecan as wsme_pecan

from pecan import rest

from stripe.common import exception
from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class QueuesController(rest.RestController):

    @wsme_pecan.wsexpose([unicode])
    def get_all(self):
        return pecan.request.db_api.get_queue_list()

    @pecan.expose()
    def get_one(self, id):
        try:
            result = pecan.request.db_api.get_queue(id)
        except exception.QueueNotFound:
            pecan.abort(404)

        return result
