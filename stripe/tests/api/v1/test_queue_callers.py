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

from stripe.tests.api.v1 import base
from stripe.tests import utils


class TestQueueCallersEmpty(base.FunctionalTest):

    def setUp(self):
        super(TestQueueCallersEmpty, self).setUp()
        queue = utils.get_test_queue()
        self.db_api.create_queue(queue)

    def test_empty_get_all(self):
        res = self.get_json('/queues/123/callers')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/queues/123/callers/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 500)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        queue_id = 1
        queue = utils.get_test_queue(id=queue_id)
        self.db_api.create_queue(queue)

    def test_create_queue_caller(self):
        self._create_queue_caller(queue_id=1)

    def test_delete_queue_caller(self):
        callers = self._create_queue_caller(queue_id=1)
        self.delete(
            '/queues/%s/callers/%s' % (
                callers[0]['queue_id'],
                callers[0]['id'],
            ), status=200
        )

        callers.pop(0)
        self._list_queue_callers(callers)

    def test_list_queue_callers(self):
        callers = self._create_queue_caller(queue_id=1)
        self._list_queue_callers(callers)

    def _list_queue_callers(self, callers):
        res = self.get_json('/queues/%s/callers' % (
            callers[0]['queue_id']
        ))
        self.assertEqual(len(res), len(callers))

        for idx in range(len(res)):
            self._validate_db_model(
                original=callers[idx], result=res[idx]
            )

    def test_get_queue_caller(self):
        callers = self._create_queue_caller(queue_id=1)
        res = self.get_json(
            '/queues/%s/callers/%s' % (
                callers[0]['queue_id'],
                callers[0]['id'],
            )
        )
        self._validate_db_model(
            original=callers[0], result=res
        )
