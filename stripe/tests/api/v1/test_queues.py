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

from stripe.tests.api.v1 import base
from stripe.tests import utils


class TestQueuesEmpty(base.FunctionalTest):

    def test_empty_get_all(self):
        res = self.get_json('/queues')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/queues/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        self._queues = []
        for i in xrange(1, 6):
            q = self._create_test_queue(id=i)
            self._queues.append(q)
        self._queues.sort()

    def _create_test_queue(self, **kwargs):
        queue = utils.get_test_queue(**kwargs)
        self.db_api.create_queue(queue)
        return queue

    def test_list_queues(self):
        res = self.get_json('/queues')
        for idx in range(len(res)):
            self._assertEqualSchemas('queue', res[idx])
        res.sort()
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        for idx in range(len(res)):
            self._assertEqualObjects(self._queues[idx], res[idx], ignored_keys)

    def test_delete_queue(self):
        self.delete(
            '/queues/1', status=200
        )
        res = self.get_json('/queues')
        for idx in range(len(res)):
            self._assertEqualSchemas('queue', res[idx])
        res.sort()
        self._queues.pop(0)
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        for idx in range(len(res)):
            self._assertEqualObjects(self._queues[idx], res[idx], ignored_keys)

    def test_get_queue(self):
        queue = self._create_test_queue()
        res = self.get_json('/queues/%s' % queue['id'])
        self._assertEqualSchemas('queue', res)

    def test_create_queue(self):
        json = {
            'name': 'support',
            'description': 'Support queue',
        }
        res = self.post_json(
            '/queues', params=json, status=200
        )
        self._assertEqualSchemas('queue', res.json)

    def test_edit_queue(self):
        json = {
            'name': 'renamed',
        }
        res = self.get_json('/queues')
        for idx in range(len(res)):
            self._assertEqualSchemas('queue', res[idx])
        queue_id = res[0]['id']
        res = self.put_json(
            '/queues/%s' % queue_id, params=json
        )
        self._assertEqualSchemas('queue', res.json)
