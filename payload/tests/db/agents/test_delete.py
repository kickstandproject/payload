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

    def test_failure(self):
        self.assertRaises(
            exception.AgentNotFound,
            self.db_api.delete_agent,
            uuid='0eda016a-b078-4bef-94ba-1ab10fe15a7d')

    def test_success(self):
        row = {
            'project_id': '793491dd5fa8477eb2d6a820193a183b',
            'user_id': '02d99a62af974b26b510c3564ba84644'
        }
        res = self.db_api.create_agent(
            user_id=row['user_id'], project_id=row['project_id'])

        self.assertTrue(res)
        self.db_api.delete_agent(uuid=res['uuid'])
        self.assertRaises(
            exception.AgentNotFound,
            self.db_api.get_agent, res['uuid'])
