# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013-2014 PolyBeacon, Inc.
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

from payload.common import exception
from payload.openstack.common import log as logging
from payload.redis import models

LOG = logging.getLogger(__name__)


class QueueCaller(object):
    """API representation of a queue caller."""

    created_at = wtypes.text
    name = wtypes.text
    number = wtypes.text
    position = int
    uuid = wtypes.text

    def __init__(self, **kwargs):
        self.fields = vars(models.QueueCaller)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class QueueCallersController(rest.RestController):
    """REST Controller for queue callers."""

    @wsme_pecan.wsexpose([QueueCaller], wtypes.text)
    def get_all(self, queue_id):
        """Retrieve a list of queue callers."""
        res = pecan.request.redis_api.list_queue_callers(
            queue_id=queue_id)

        return res

    @wsme_pecan.wsexpose(QueueCaller, wtypes.text, wtypes.text)
    def get_one(self, queue_id, uuid):
        """Retrieve information about the given queue."""
        try:
            result = pecan.request.redis_api.get_queue_caller(
                queue_id=queue_id, uuid=uuid)
        except exception.QueueCallerNotFound:
            # TODO(pabelanger): See if there is a better way of handling
            # exceptions.
            raise wsme.exc.ClientSideError('Not found')

        return result
