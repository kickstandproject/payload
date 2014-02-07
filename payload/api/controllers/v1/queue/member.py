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
from pecan import rest
import wsme
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from payload.api.controllers.v1 import base
from payload.common import exception
# TODO(pabelanger): We should not be access db.sqlalchemy directly.
from payload.db.sqlalchemy import models
from payload.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class QueueMember(base.APIBase):
    """API representation of a queue member."""

    agent_uuid = wtypes.text
    queue_uuid = wtypes.text

    def __init__(self, **kwargs):
        self.fields = vars(models.QueueMember)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class QueueMembersController(rest.RestController):
    """REST Controller for queue members."""

    @wsme_pecan.wsexpose(None, wtypes.text, wtypes.text, status_code=204)
    def delete(self, uuid, agent_uuid):
        """Delete a queue member."""
        try:
            pecan.request.db_api.delete_queue_member(
                agent_uuid=agent_uuid, queue_uuid=uuid)
        except exception.QueueMemberNotFound as e:
            raise wsme.exc.ClientSideError(e.message, status_code=e.code)

    @wsme_pecan.wsexpose([QueueMember], wtypes.text)
    def get_all(self, uuid):
        """Retrieve a list of queue members."""
        res = pecan.request.db_api.list_queue_members(uuid=uuid)

        return res

    @wsme_pecan.wsexpose(QueueMember, wtypes.text, wtypes.text)
    def get_one(self, uuid, agent_uuid):
        """Retrieve information about the given queue member."""
        try:
            res = pecan.request.db_api.get_queue_member(
                agent_uuid=agent_uuid, queue_uuid=uuid)
        except exception.QueueMemberNotFound as e:
            raise wsme.exc.ClientSideError(e.message, status_code=e.code)
        return res

    @wsme.validate(QueueMember)
    @wsme_pecan.wsexpose(
        QueueMember, wtypes.text, body=QueueMember, status_code=200)
    def post(self, uuid, body):
        """Create a new queue member."""
        d = body.as_dict()
        res = pecan.request.db_api.create_queue_member(
            agent_uuid=d['agent_uuid'], queue_uuid=uuid)

        return res
