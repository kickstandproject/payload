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

    def test_create_queue(self):
        self._create_test_queue()

    def test_delete_queue(self):
        res = self._create_test_queue()
        self.delete(
            '/queues/%s' % res['id'], status=204
        )
        self._list_queues([])

    def test_get_queue(self):
        queue = self._create_test_queue()
        res = self.get_json('/queues/%s' % queue['id'])
        self._assertEqualSchemas('queue', res)

    def test_list_queues(self):
        queue = self._create_test_queue()
        self._list_queues([queue])

    def test_edit_queue(self):
        queue = self._create_test_queue()
        json = {
            'name': 'renamed',
        }
        res = self.put_json(
            '/queues/%s' % queue['id'], params=json
        )
        self._assertEqualSchemas('queue', res.json)

    def _list_queues(self, queues):
        res = self.get_json('/queues')
        self.assertEqual(res, queues)
