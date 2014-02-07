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

import datetime

from payload.openstack.common import uuidutils
from payload.tests.db import base


class TestCase(base.FunctionalTest):

    def test_success(self):
        row = {
            'id': 1,
            'project_id': '793491dd5fa8477eb2d6a820193a183b',
            'updated_at': None,
            'user_id': '02d99a62af974b26b510c3564ba84644'
        }
        self.db_api.create_agent(
            user_id=row['user_id'], project_id=row['project_id'])

        res = self.db_api.list_agents()

        self.assertEqual(len(res), 1)

        for k, v in row.iteritems():
            self.assertEqual(res[0][k], v)

        self.assertEqual(type(res[0]['created_at']), datetime.datetime)
        self.assertTrue(uuidutils.is_uuid_like(res[0]['uuid']))

        # NOTE(pabelanger): We add 3 because of created_at, uuid, and hidden
        # sqlalchemy object.
        self.assertEqual(len(res[0].__dict__), len(row) + 3)
