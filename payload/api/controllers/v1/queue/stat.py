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
from wsmeext import pecan as wsme_pecan

from payload.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class QueueStatsController(rest.RestController):
    """REST Controller for queue stats."""

    @wsme_pecan.wsexpose(unicode, unicode)
    def get_all(self, queue_id):
        """Retrieve a list of queue stats."""
        res = pecan.request.middleware_api.get_queue_stats(queue_id)

        return res
