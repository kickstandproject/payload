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

from payload.tests.db import base


class TestCase(base.FunctionalTest):

    def test_all_fields(self):
        row = {
            'agent_uuid': '793491dd5fa8477eb2d6a820193a183b',
            'id': 1,
            'queue_uuid': '02d99a62af974b26b510c3564ba84644',
            'updated_at': None,
        }
        res = self.db_api.create_queue_member(
            agent_uuid=row['agent_uuid'], queue_uuid=row['queue_uuid'])

        for k, v in row.iteritems():
            self.assertEqual(res[k], v)

        self.assertEqual(type(res['created_at']), datetime.datetime)

        # NOTE(pabelanger): We add 2 because of created_at and hidden
        # sqlalchemy object.
        self.assertEqual(len(res.__dict__), len(row) + 2)

    def test_required_fields(self):
        row = {
            'agent_uuid': '793491dd5fa8477eb2d6a820193a183b',
            'id': 1,
            'queue_uuid': '02d99a62af974b26b510c3564ba84644',
            'updated_at': None,
        }
        res = self.db_api.create_queue_member(
            agent_uuid=row['agent_uuid'], queue_uuid=row['queue_uuid'])

        for k, v in row.iteritems():
            self.assertEqual(res[k], v)

        self.assertEqual(type(res['created_at']), datetime.datetime)

        # NOTE(pabelanger): We add 2 because of created_at and hidden
        # sqlalchemy object.
        self.assertEqual(len(res.__dict__), len(row) + 2)
