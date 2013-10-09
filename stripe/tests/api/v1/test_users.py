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


class TestUsersEmpty(base.FunctionalTest):

    def test_empty_get_all(self):
        res = self.get_json('/users')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/users/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def test_create_user(self):
        self._create_test_user()

    def test_delete_user(self):
        res = self._create_test_user()
        self.delete(
            '/users/%s' % res['id'], status=204
        )
        self._list_users([])

    def test_get_user(self):
        user = self._create_test_user()
        res = self.get_json('/users/%s' % user['id'])
        self._assertEqualSchemas('user', res)

    def test_list_users(self):
        user = self._create_test_user()
        self._list_users([user])

    def test_edit_user(self):
        user = self._create_test_user()
        json = {
            'name': 'renamed',
        }
        res = self.put_json(
            '/users/%s' % user['id'], params=json
        )
        self._assertEqualSchemas('user', res.json)

    def _list_users(self, users):
        res = self.get_json('/users')
        self.assertEqual(res, users)
