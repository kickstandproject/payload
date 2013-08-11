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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pecan
import wsme

from pecan import rest
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from stripe.api.controllers.v1 import base
from stripe.db import models
from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class QueueMember(base.APIBase):
    """API representation of a queue member."""

    id = int
    agent_id = int
    queue_id = int

    def __init__(self, **kwargs):
        self.fields = vars(models.QueueMember)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class QueueMembersController(rest.RestController):
    """REST Controller for queue members."""

    @wsme_pecan.wsexpose(None, wtypes.text, wtypes.text, status_code=204)
    def delete(self, queue_id, id):
        """Delete a queue member."""
        pecan.request.db_api.delete_queue_member(id)

    @wsme_pecan.wsexpose([QueueMember], wtypes.text)
    def get_all(self, queue_id):
        """Retrieve a list of queue members."""
        res = pecan.request.db_api.list_queue_members()

        return res

    @wsme_pecan.wsexpose(QueueMember, wtypes.text, wtypes.text)
    def get_one(self, queue_id, id):
        """Retrieve information about the given queue member."""
        res = pecan.request.db_api.get_queue_member(id)

        return res

    @wsme.validate(QueueMember)
    @wsme_pecan.wsexpose(QueueMember, wtypes.text, body=QueueMember)
    def post(self, queue_id, body):
        """Create a new queue member."""
        res = pecan.request.db_api.create_queue_member(body.as_dict())

        return res
