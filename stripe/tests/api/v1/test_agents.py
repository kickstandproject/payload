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

    def test_create_agent(self):
        self._create_test_agent()

    def test_delete_agent(self):
        res = self._create_test_agent()
        self.delete(
            '/agents/%s' % res['id'], status=200
        )
        self._list_agents([])

    def test_edit_agent(self):
        agent = self._create_test_agent()
        json = {
            'name': 'renamed',
        }
        res = self.put_json(
            '/agents/%s' % agent['id'], params=json
        )
        self._assertEqualSchemas('agent', res.json)

    def test_get_agent(self):
        agent = self._create_test_agent()
        res = self.get_json('/agents/%s' % agent['id'])
        self._assertEqualSchemas('agent', res)

    def test_list_agents(self):
        res = self._create_test_agent()
        self._list_agents([res])

    def _list_agents(self, agents):
        res = self.get_json('/agents')
        self.assertEqual(res, agents)
