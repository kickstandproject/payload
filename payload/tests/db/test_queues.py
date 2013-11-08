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

from payload.common import exception
from payload.tests.db import base


class TestCase(base.FunctionalTest):

    def test_create_queue(self):
        self._create_test_queue()

    def test_delete_queue(self):
        queue = self._create_test_queue()
        self.db_api.delete_queue(uuid=queue['uuid'])
        self.assertRaises(
            exception.QueueNotFound, self.db_api.get_queue, queue['uuid']
        )

    def test_delete_queue_not_found(self):
        self.assertRaises(
            exception.QueueNotFound, self.db_api.delete_queue, 123
        )

    def test_get_queue_by_id(self):
        queue = self._create_test_queue()
        res = self.db_api.get_queue(uuid=queue['uuid'])
        self.assertEqual(queue['uuid'], res['uuid'])

    def test_list_queues(self):
        queue = []
        for i in xrange(1, 6):
            q = self._create_test_queue(uuid=i)
            queue.append(q)
        res = self.db_api.list_queues()
        res.sort()
        queue.sort()
        self.assertEqual(len(res), len(queue))
