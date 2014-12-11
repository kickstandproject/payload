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

from payload.common import exception
from payload.openstack.common import log as logging
from payload.redis import models

LOG = logging.getLogger(__name__)


class QueueMember(object):
    """API representation of a queue member."""

    created_at = wtypes.text
    number = wtypes.text
    paused = wtypes.text
    paused_at = wtypes.text
    status = wtypes.text
    status_at = wtypes.text
    uuid = wtypes.text

    def __init__(self, **kwargs):
        self.fields = vars(models.QueueMember)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class QueueMembersController(rest.RestController):
    """REST Controller for queue members."""

    @wsme_pecan.wsexpose([QueueMember], wtypes.text)
    def get_all(self, queue_id):
        """Retrieve a list of queue members."""
        res = pecan.request.redis_api.list_queue_members(queue_id=queue_id)

        return res

    @wsme_pecan.wsexpose(QueueMember, wtypes.text, wtypes.text)
    def get_one(self, queue_id, uuid):
        """Retrieve information about the given queue member."""
        try:
            res = pecan.request.redis_api.get_queue_member(
                queue_id=queue_id, uuid=uuid)
        except exception.QueueMemberNotFound as e:
            raise wsme.exc.ClientSideError(e.message, status_code=e.code)
        return res
