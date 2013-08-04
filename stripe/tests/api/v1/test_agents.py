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


class TestAgentsEmpty(base.FunctionalTest):

    def test_empty_get_all(self):
        res = self.get_json('/agents')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/agents/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        self._agents = []
        for i in xrange(1, 6):
            m = self._create_test_agent(id=i)
            self._agents.append(m)
        self._agents.sort()

    def _create_test_agent(self, **kwargs):
        agent = utils.get_test_agent(**kwargs)
        self.db_api.create_agent(agent)
        return agent

    def test_list_agents(self):
        res = self.get_json('/agents')
        for idx in range(len(res)):
            self._assertEqualSchemas('agent', res[idx])

        res.sort()
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        for idx in range(len(res)):
            self._assertEqualObjects(
                self._agents[idx], res[idx], ignored_keys
            )

    def test_delete_agent(self):
        self.delete(
            '/agents/1', status=200
        )
        res = self.get_json('/agents')
        for idx in range(len(res)):
            self._assertEqualSchemas('agent', res[idx])
        res.sort()
        self._agents.pop(0)
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        for idx in range(len(res)):
            self._assertEqualObjects(
                self._agents[idx], res[idx], ignored_keys
            )

    def test_get_agent(self):
        agent = self._create_test_agent()
        res = self.get_json('/agents/%s' % agent['id'])
        self._assertEqualSchemas('agent', res)

    def test_create_agent(self):
        json = {
            'name': 'Jane Doe',
            'password': 'example',
        }
        res = self.post_json(
            '/agents', params=json, status=200
        )
        self._assertEqualSchemas('agent', res.json)

    def test_edit_agent(self):
        json = {
            'name': 'renamed',
        }
        res = self.get_json('/agents')
        for idx in range(len(res)):
            self._assertEqualSchemas('agent', res[idx])
        agent_id = res[0]['id']
        res = self.put_json(
            '/agents/%s' % agent_id, params=json
        )
        self._assertEqualSchemas('agent', res.json)
