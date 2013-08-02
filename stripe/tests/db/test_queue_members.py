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

from stripe.common import exception
from stripe.tests.db import base


class TestCase(base.FunctionalTest):

    def test_create_queue_member(self):
        res = self._create_test_queue_member()
        self.assertTrue(res)

    def test_create_queue_member_duplicate(self):
        self._create_test_queue_member(id=1)
        self.assertRaises(
            exception.QueueMemberDuplicated, self._create_test_queue_member,
            id=2,
        )

    def test_delete_queue_member(self):
        queue_member = self._create_test_queue_member()
        self.db_api.delete_queue_member(queue_member['id'])
        self.assertRaises(
            exception.QueueMemberNotFound, self.db_api.get_queue_member,
            queue_member['id'],
        )

    def test_delete_queue_member_not_found(self):
        self.assertRaises(
            exception.QueueMemberNotFound, self.db_api.delete_queue_member, 123
        )

    def test_get_queue_member_by_id(self):
        queue_member = self._create_test_queue_member()
        res = self.db_api.get_queue_member(queue_member['id'])
        self.assertEqual(queue_member['id'], res['id'])

    def test_get_queue_member_list(self):
        queue_member = []
        for i in xrange(1, 2):
            qm = self._create_test_queue_member(id=i, member_id=i)
            queue_member.append(qm['id'])
        res = self.db_api.get_queue_member_list()
        res.sort()
        queue_member.sort()
        self.assertEqual(len(res), len(queue_member))

    def test_get_queue_member_list_by_queue_id(self):
        queue_member = []
        queue_id = 1
        for i in xrange(1, 2):
            self._create_test_queue_member(id=i, member_id=i)

        for i in xrange(3, 4):
            qm = self._create_test_queue_member(
                id=i, member_id=i, queue_id=queue_id
            )
            queue_member.append(qm['id'])

        res = self.db_api.get_queue_member_list(queue_id=queue_id)
        res.sort()
        queue_member.sort()
        self.assertEqual(len(res), len(queue_member))
