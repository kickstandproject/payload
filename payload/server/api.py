# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from payload.cache import api
from payload.cache.api import QueueCallerStatus
from payload.cache.api import QueueMemberStatus


class API(object):

    def __init__(self):
        self.cache_api = api.get_instance()

    def get_available_queue_caller(self, queue_id):
        callers = self.cache_api.list_queue_callers(
            queue_id=queue_id, status=QueueCallerStatus.WAITING)

        if any(callers):
            return callers[0].uuid

        return None

    def get_available_queue_member(self, queue_id):
        members = self.cache_api.list_queue_members(
            queue_id=queue_id, status=QueueMemberStatus.WAITING)

        if any(members):
            return members[0].uuid

        return None
