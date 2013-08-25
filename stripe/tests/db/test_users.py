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

from stripe.common import exception
from stripe.tests.db import base


class TestCase(base.FunctionalTest):

    def test_create_user(self):
        self._create_test_user()

    def test_delete_user(self):
        user = self._create_test_user()
        self.db_api.delete_user(user['id'])
        self.assertRaises(
            exception.UserNotFound, self.db_api.get_user, user['id']
        )

    def test_delete_user_not_found(self):
        self.assertRaises(
            exception.UserNotFound, self.db_api.delete_user, 123
        )

    def test_get_user_by_id(self):
        user = self._create_test_user()
        res = self.db_api.get_user(user['id'])
        self.assertEqual(user['id'], res['id'])

    def test_list_users(self):
        user = []
        for i in xrange(1, 6):
            q = self._create_test_user(id=i)
            user.append(q)
        res = self.db_api.list_users()
        res.sort()
        user.sort()
        self.assertEqual(len(res), len(user))
