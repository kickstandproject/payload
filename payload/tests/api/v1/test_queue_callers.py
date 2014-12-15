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

from payload.cache import api
from payload.tests.api.v1 import base


class TestQueueCallersEmpty(base.FunctionalTest):

    def setUp(self):
        super(TestQueueCallersEmpty, self).setUp()
        self._create_test_queue()

    def test_empty_get_all(self):
        res = self.get_json('/queues/123/callers')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/queues/123/callers/1', expect_errors=True)
        self.assertEqual(res.status_int, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        self.cache_api = api.get_instance()
        res = self._create_test_queue()
        self.queue_id = res['uuid']

    def test_create_queue_caller(self):
        self._create_queue_caller(queue_id=self.queue_id)

    def test_list_queue_callers(self):
        callers = self._create_queue_caller(queue_id=self.queue_id)
        self._list_queue_callers([callers.__dict__])

    def test_get_queue_caller(self):
        caller = self._create_queue_caller(queue_id=self.queue_id)
        res = self.get_json(
            '/queues/%s/callers/%s' % (
                self.queue_id, caller.uuid,
            )
        )
        self.assertEqual(caller.uuid, res['uuid'])

    def _list_queue_callers(self, callers):
        res = self.get_json('/queues/%s/callers' % self.queue_id)
        self.assertEqual(res, callers)

    def _create_queue_caller(self, queue_id):
        res = self.cache_api.create_queue_caller(
            queue_id=queue_id, uuid='1234', name='Bob Smith',
            number='6135551234')

        return res
