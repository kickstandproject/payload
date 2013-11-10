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

from payload.tests.api.v1 import base


class TestQueueMembersEmpty(base.FunctionalTest):

    def setUp(self):
        super(TestQueueMembersEmpty, self).setUp()
        self._create_test_queue()

    def test_empty_get_all(self):
        res = self.get_json('/queues/123/members')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/queues/123/members/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        agent = self._create_test_agent()
        self.agent_uuid = agent['uuid']
        queue = self._create_test_queue()
        self.queue_uuid = queue['uuid']

    def test_create_queue_member(self):
        self._create_test_queue_member()

    def test_delete_queue_member(self):
        self._create_test_queue_member()
        self.delete(
            '/queues/%s/members/%s' % (
                self.queue_uuid, self.agent_uuid
            ), status=204)

        self._list_queue_members([])

    def test_get_queue_member(self):
        self._create_test_queue_member()
        res = self.get_json(
            '/queues/%s/members/%s' % (
                self.queue_uuid, self.agent_uuid
            ), expect_errors=True)
        self.assertEqual(res.status_int, 204)

    def test_list_queue_members(self):
        self._create_test_queue_member()
        res = {
            'agent_uuid': self.agent_uuid,
            'queue_uuid': self.queue_uuid,
        }
        self._list_queue_members([res])

    def _create_test_queue_member(self):
        res = self.post_json(
            '/queues/%s/members/%s' % (
                self.queue_uuid, self.agent_uuid
            ), status=204)
        self.assertEqual(res.status_int, 204)

    def _list_queue_members(self, members):
        res = self.get_json('/queues/%s/members' % self.queue_uuid)
        self.assertEqual(len(res), len(members))
