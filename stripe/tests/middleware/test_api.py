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

from stripe.tests.middleware import base


class TestCase(base.TestCase):

    def test_create_queue_caller(self):
        self._create_queue_caller(queue_id=1)

    def test_create_queue_member(self):
        self._create_queue_member(queue_id=1)

    def test_delete_queue_member(self):
        members = self._create_queue_member()

        self.middleware_api.delete_queue_member(
            id=members[0]['id'],
            queue_id=members[0]['queue_id'],
        )

        members.pop(0)
        self._list_queue_members(members)

    def test_list_queue_callers(self):
        queue_id = 1
        callers = self._create_queue_caller(queue_id=queue_id)
        self._list_queue_callers(callers, queue_id)

    def _list_queue_callers(self, callers, queue_id):
        res = self.middleware_api.list_queue_callers(
            queue_id=queue_id,
            state='onhold',
        )
        self.assertEqual(len(res), len(callers))

    def test_list_queue_members(self):
        members = self._create_queue_member(queue_id=1)
        self._list_queue_members(members)

    def _list_queue_members(self, members):
        res = self.middleware_api.list_queue_members(
            members[0]['queue_id']
        )
        self.assertEqual(len(res), len(members))

        for idx in range(len(res)):
            self._validate_db_model(
                original=members[idx], result=res[idx]
            )

    def test_get_queue_callers(self):
        queue_id = 1
        callers = self._create_queue_caller(queue_id=queue_id)
        res = self.middleware_api.get_queue_caller(
            uuid=callers[0],
            queue_id=queue_id,
        )
        self.assertEqual(res['uuid'], callers[0])

    def test_get_queue_member(self):
        members = self._create_queue_member(queue_id=1)
        res = self.middleware_api.get_queue_member(
            id=members[0]['id'],
            queue_id=members[0]['queue_id'],
        )
        self._validate_db_model(
            original=members[0], result=res
        )
