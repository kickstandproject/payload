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


class TestCase(base.FunctionalTest):

    def test_failure(self):
        res = self.delete(
            '/queues/%s/members/%s' % (
                '0eda016a-b078-4bef-94ba-1ab10fe15a7d',
                '0eda016a-b078-4bef-94ba-1ab10fe15a7d'
            ), status=404, expect_errors=True)

        self.assertEqual(res.status_int, 404)
        self.assertTrue(res.json['error_message'])

    def test_success(self):
        json = {
            'description': '24/7 support',
            'disabled': True,
            'name': 'support',
            'project_id': '5fccabbb-9d65-417f-8b0b-a2fc77b501e6',
            'updated_at': None,
            'user_id': '09f07543-6dad-441b-acbf-1c61b5f4015e',
        }
        params = {
            'description': json['description'],
            'disabled': json['disabled'],
            'name': json['name'],
        }
        headers = {
            'X-User-Id': json['user_id'],
            'X-Tenant-Id': json['project_id'],
        }
        queue = self.post_json(
            '/queues', params=params, status=200, headers=headers)
        self.assertTrue(queue)

        json = {
            'project_id': '5fccabbb-9d65-417f-8b0b-a2fc77b501e6',
            'updated_at': None,
            'user_id': '09f07543-6dad-441b-acbf-1c61b5f4015e',
        }
        agent = self.post_json(
            '/agents', params=json, status=200, headers=self.auth_headers)
        self.assertTrue(agent)

        json = {
            'agent_uuid': agent['uuid'],
        }
        res = self.post_json(
            '/queues/%s/members' % queue['uuid'], params=json, status=200,
            headers=self.auth_headers)
        self.assertTrue(res)

        self.delete(
            '/queues/%s/members/%s' % (queue['uuid'], agent['uuid']),
            status=204)
        res = self.get_json(
            '/queues/%s/members/%s' % (queue['uuid'], agent['uuid']),
            expect_errors=True)
        self.assertEqual(res.status_int, 404)
        self.assertTrue(res.json['error_message'])
