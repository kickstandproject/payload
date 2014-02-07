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

from payload.openstack.common import uuidutils
from payload.tests.api.v1 import base


class TestCase(base.FunctionalTest):

    def test_all_fields(self):
        json = {
            'project_id': '5fccabbb-9d65-417f-8b0b-a2fc77b501e6',
            'updated_at': None,
            'user_id': '09f07543-6dad-441b-acbf-1c61b5f4015e',
        }

        res = self.post_json(
            '/agents', params=json, status=200, headers=self.auth_headers)

        for k, v in json.iteritems():
            self.assertEqual(res[k], v)

        self.assertTrue(res['created_at'])
        self.assertTrue(uuidutils.is_uuid_like(res['uuid']))

        # NOTE(pabelanger): We add 2 because of created_at and uuid
        self.assertEqual(len(res), len(json) + 2)
