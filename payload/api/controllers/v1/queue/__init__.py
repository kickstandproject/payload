# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
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

from payload.api.controllers.v1 import base
from payload.api.controllers.v1.queue import caller
from payload.api.controllers.v1.queue import member
from payload.api.controllers.v1.queue import stat
from payload.common import exception
from payload.db import models
from payload.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class Queue(base.APIBase):
    """API representation of a queue."""

    description = wtypes.text
    disabled = bool
    name = wtypes.text
    project_id = wtypes.text
    user_id = wtypes.text
    uuid = wtypes.text

    def __init__(self, **kwargs):
        self.fields = vars(models.Queue)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class QueuesController(rest.RestController):
    """REST Controller for queues."""

    callers = caller.QueueCallersController()
    members = member.QueueMembersController()
    stats = stat.QueueStatsController()

    @wsme_pecan.wsexpose(None, wtypes.text, status_code=204)
    def delete(self, uuid):
        """Delete a queue."""
        try:
            pecan.request.db_api.delete_queue(uuid=uuid)
        except exception.QueueNotFound as e:
            raise wsme.exc.ClientSideError(e.message, status_code=e.code)

    @wsme_pecan.wsexpose([Queue])
    def get_all(self):
        """Retrieve a list of queues."""

        return pecan.request.db_api.list_queues()

    @wsme_pecan.wsexpose(Queue, unicode)
    def get_one(self, uuid):
        """Retrieve information about the given queue."""
        try:
            result = pecan.request.db_api.get_queue(uuid=uuid)
        except exception.QueueNotFound as e:
            # TODO(pabelanger): See if there is a better way of handling
            # exceptions.
            raise wsme.exc.ClientSideError(e.message, status_code=e.code)

        return result

    @wsme.validate(Queue)
    @wsme_pecan.wsexpose(Queue, body=Queue)
    def post(self, body):
        """Create a new queue."""
        user_id = pecan.request.headers.get('X-User-Id')
        project_id = pecan.request.headers.get('X-Tenant-Id')
        d = body.as_dict()
        res = pecan.request.db_api.create_queue(
            name=d['name'], user_id=user_id, project_id=project_id,
            description=d['description'], disabled=d['disabled'])
        return res

    @wsme.validate(Queue)
    @wsme_pecan.wsexpose(Queue, wtypes.text, body=Queue)
    def put(self, uuid, body):
        queue = pecan.request.db_api.get_queue(uuid)
        items = body.as_dict().items()
        for k, v in [(k, v) for (k, v) in items if v]:
            queue[k] = v

        queue.save()
        return queue
