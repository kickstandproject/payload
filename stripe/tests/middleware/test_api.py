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

from stripe.middleware import api
from stripe.tests.middleware import base


class TestCase(base.TestCase):

    def test_create_queue_caller(self):
        self._create_queue_caller(queue_id=1)

    def test_list_queue_callers(self):
        queue_id = 1
        callers = self._create_queue_caller(queue_id=queue_id)
        self._list_queue_callers(len(callers), queue_id)

    def _list_queue_callers(self, total_callers, queue_id, status=None):
        res = self.middleware_api.list_queue_callers(
            queue_id=queue_id,
            status=status,
        )
        self.assertEqual(len(res), total_callers)

    def test_get_queue_callers(self):
        queue_id = 1
        callers = self._create_queue_caller(queue_id=queue_id)
        res = self.middleware_api.get_queue_caller(
            uuid=callers[0],
            queue_id=queue_id,
        )
        self.assertEqual(res['uuid'], callers[0])

    def test_set_queue_caller_status(self):
        queue_id = 1
        status = api.QueueCallerStatus.RINGING
        callers = self._create_queue_caller(queue_id=queue_id)
        self.middleware_api.set_queue_caller_status(
            queue_id=queue_id, status=status,
            uuid=callers[0],
        )
        res = self.middleware_api.get_queue_caller(
            uuid=callers[0],
            queue_id=queue_id,
        )
        self.assertEqual(res['uuid'], callers[0])
        self.assertEqual(res['status'], unicode(status))
        self.assertEqual(res['queue_id'], unicode(queue_id))
        callers.pop(0)
        self._list_queue_callers(len(callers), queue_id)
        self._list_queue_callers(1, queue_id, status=status)
