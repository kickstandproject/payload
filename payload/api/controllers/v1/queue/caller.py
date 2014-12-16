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

from pecan import rest
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from payload.cache import models
from payload.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class QueueCaller(object):
    """API representation of a queue caller."""

    created_at = wtypes.text
    name = wtypes.text
    number = wtypes.text
    position = int
    queue_id = wtypes.text
    uuid = wtypes.text

    def __init__(self, **kwargs):
        self.fields = vars(models.QueueCaller)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class QueueCallersController(rest.RestController):
    """REST Controller for queue callers."""

    @wsme_pecan.wsexpose([QueueCaller], wtypes.text)
    def get_all(self, queue_id):
        """List callers from the specified queue.

        .. http:get:: /queues/:queue_uuid/callers

           **Example request**:

           .. sourcecode:: http

              GET /queues/cc096e0b-0c96-4b8b-b812-ef456f361ee3/callers

           **Example response**:

           .. sourcecode:: http

              [
                {
                  "created_at": "2014-12-12T02:05:14Z",
                  "name": "Paul Belanger",
                  "number": "6135551234",
                  "position": 0,
                  "queue_id": "cc096e0b-0c96-4b8b-b812-ef456f361ee3",
                  "uuid": "e5814fee-6e8a-4771-8edd-ea413eff57f1",
                },
                {
                  "created_at": "2014-12-12T02:07:05Z",
                  "name": "Leif Madsen",
                  "number": "9055555678",
                  "position": 1,
                  "queue_id": "cc096e0b-0c96-4b8b-b812-ef456f361ee3",
                  "uuid": "4b4fa110-be14-45b7-a998-2219ab8bee6f",
                }
              ]
        """
        res = pecan.request.cache_api.list_queue_callers(
            queue_id=queue_id)

        return res

    @wsme_pecan.wsexpose(QueueCaller, wtypes.text, wtypes.text)
    def get_one(self, queue_id, uuid):
        """Get a single caller from the specified queue.

        .. http:get:: /queues/:queue_uuid/callers/:caller_uuid

           **Example request**:

           .. sourcecode:: http

              GET /queues/cc096e0b-0c96-4b8b-b812-ef456f361ee3/callers/\
e5814fee-6e8a-4771-8edd-ea413eff57f1

           **Example response**:

           .. sourcecode:: http

              {
                "created_at": "2014-12-12T02:05:14Z",
                "name": "Paul Belanger",
                "number": "6135551234",
                "position": 0,
                "queue_id": "cc096e0b-0c96-4b8b-b812-ef456f361ee3",
                "uuid": "e5814fee-6e8a-4771-8edd-ea413eff57f1",
              }
        """
        result = pecan.request.cache_api.get_queue_caller(
            queue_id=queue_id, uuid=uuid)

        return result
