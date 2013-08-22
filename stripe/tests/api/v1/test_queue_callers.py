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


class TestQueueCallersEmpty(base.FunctionalTest):

    def setUp(self):
        super(TestQueueCallersEmpty, self).setUp()
        self._create_test_queue()

    def test_empty_get_all(self):
        res = self.get_json('/queues/123/callers')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/queues/123/callers/1', expect_errors=True
        )
        self.assertEqual(res.json, {})


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        res = self._create_test_queue()
        self.queue_id = res['id']

    def test_create_queue_caller(self):
        self._create_queue_caller()

    def test_delete_queue_caller(self):
        callers = self._create_queue_caller()
        self.delete(
            '/queues/%s/callers/%s' % (
                self.queue_id, callers['uuid']
            ), status=200,
        )
        self._list_queue_callers([])

    def test_list_queue_callers(self):
        callers = self._create_queue_caller()
        self._list_queue_callers([callers])

    def test_get_queue_caller(self):
        callers = self._create_queue_caller()
        res = self.get_json(
            '/queues/%s/callers/%s' % (
                self.queue_id, callers['uuid'],
            )
        )
        self.assertEqual(callers['uuid'], res['uuid'])

    def _create_queue_caller(self):
        json = utils.get_test_queue_caller(queue_id=self.queue_id)
        res = self.post_json(
            '/queues/%s/callers' % self.queue_id, params=json, status=200
        )
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')

        return res.json

    def _list_queue_callers(self, callers):
        res = self.get_json('/queues/%s/callers' % self.queue_id)
        self.assertEqual(res, callers)
