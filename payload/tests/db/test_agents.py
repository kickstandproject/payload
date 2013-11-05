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

    def test_create_agent(self):
        self._create_test_agent()

    def test_delete_agent(self):
        agent = self._create_test_agent()
        self.db_api.delete_agent(agent['id'])
        self.assertRaises(
            exception.AgentNotFound, self.db_api.get_agent, agent['id']
        )

    def test_delete_agent_not_found(self):
        self.assertRaises(
            exception.AgentNotFound, self.db_api.delete_agent, 123
        )

    def test_list_agents(self):
        agent = []
        for i in xrange(1, 6):
            q = self._create_test_agent(id=i)
            agent.append(q)
        res = self.db_api.list_agents()
        res.sort()
        agent.sort()
        self.assertEqual(len(res), len(agent))
