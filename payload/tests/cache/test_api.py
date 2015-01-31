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

from payload.cache import api
from payload.common import exception
from payload.tests import base


class TestCase(base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.cache_api = api.get_instance()

    def test_create_queue_caller(self):
        self._create_queue_caller()

    def test_create_queue_member(self):
        self._create_queue_member()

    def test_delete_queue_caller(self):
        caller = self._create_queue_caller()

        self.cache_api.delete_queue_caller(
            queue_id=caller['queue_id'], uuid=caller['uuid'])

        self.assertRaises(
            exception.QueueCallerNotFound,
            self.cache_api.get_queue_caller,
            queue_id=caller['queue_id'], uuid=caller['uuid'])

    def test_delete_queue_member(self):
        member = self._create_queue_member()

        self.cache_api.delete_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid'])

        self.assertRaises(
            exception.QueueMemberNotFound,
            self.cache_api.get_queue_member,
            queue_id=member['queue_id'], uuid=member['uuid'])

    def test_list_queue_callers(self):
        callers = dict()
        for x in range(0, 2):
            callers[x] = self._create_queue_caller()

        res = self.cache_api.list_queue_callers(
            queue_id=callers[0]['queue_id'])

        self.assertEqual(len(res), 2)

        res = self.cache_api.list_queue_callers(
            queue_id=callers[0]['queue_id'],
            status=api.QueueCallerStatus.WAITING)
        self.assertEqual(len(res), 2)

        self.cache_api.update_queue_caller(
            queue_id=callers[0]['queue_id'], uuid=callers[0]['uuid'],
            status=api.QueueCallerStatus.RINGING)

        res = self.cache_api.list_queue_callers(
            queue_id=callers[0]['queue_id'],
            status=api.QueueCallerStatus.WAITING)
        self.assertEqual(len(res), 1)

        res = self.cache_api.list_queue_callers(
            queue_id=callers[0]['queue_id'],
            status=api.QueueCallerStatus.RINGING)
        self.assertEqual(len(res), 1)

    def test_list_queue_member(self):
        members = dict()
        for x in range(0, 2):
            members[x] = self._create_queue_member()

        res = self.cache_api.list_queue_members(
            queue_id=members[0]['queue_id'])

        self.assertEqual(len(res), 2)

        res = self.cache_api.list_queue_members(
            queue_id=members[0]['queue_id'],
            status=api.QueueMemberStatus.WAITING)
        self.assertEqual(len(res), 2)

        self.cache_api.update_queue_member(
            queue_id=members[0]['queue_id'], uuid=members[0]['uuid'],
            status=api.QueueMemberStatus.RINGING)

        res = self.cache_api.list_queue_members(
            queue_id=members[0]['queue_id'],
            status=api.QueueMemberStatus.WAITING)
        self.assertEqual(len(res), 1)

        res = self.cache_api.list_queue_members(
            queue_id=members[0]['queue_id'],
            status=api.QueueMemberStatus.RINGING)
        self.assertEqual(len(res), 1)

    def test_update_queue_caller(self):
        caller = self._create_queue_caller()

        self.cache_api.update_queue_caller(
            queue_id=caller['queue_id'], uuid=caller['uuid'],
            member_uuid='9876', name='Jim', number='1234', status=3)

        res = self.cache_api.get_queue_caller(
            queue_id=caller['queue_id'], uuid=caller['uuid']).__dict__

        self.assertEqual(res['name'], 'Jim')
        self.assertEqual(res['number'], '1234')
        self.assertEqual(res['status'], '3')
        self.assertEqual(res['member_uuid'], '9876')
        self.assertGreater(res['status_at'], caller['status_at'])

        self.assertRaises(
            exception.QueueCallerNotFound,
            self.cache_api.update_queue_caller,
            queue_id='foo', uuid='bar', member_uuid='9876', name='Jim',
            number='1234', status=3)

    def test_update_queue_caller_only_status(self):
        caller = self._create_queue_caller()

        self.cache_api.update_queue_caller(
            queue_id=caller['queue_id'], uuid=caller['uuid'], status=3)

        res = self.cache_api.get_queue_caller(
            queue_id=caller['queue_id'], uuid=caller['uuid']).__dict__

        self.assertEqual(res['status'], '3')
        self.assertGreater(res['status_at'], caller['status_at'])

    def test_update_queue_member(self):
        member = self._create_queue_member()

        self.cache_api.update_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid'],
            number='1234', paused=1, status=3)

        res = self.cache_api.get_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid']).__dict__

        self.assertEqual(res['number'], '1234')
        self.assertEqual(res['paused'], '1')
        self.assertEqual(res['status'], '3')
        self.assertGreater(res['status_at'], member['status_at'])

        self.assertRaises(
            exception.QueueMemberNotFound,
            self.cache_api.update_queue_member,
            queue_id='foo', uuid='bar', number='1234', paused=1, status=3)

    def test_update_queue_member_paused(self):
        member = self._create_queue_member()

        self.cache_api.update_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid'],
            paused=1)

        res = self.cache_api.get_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid']).__dict__

        self.assertEqual(res['paused'], '1')
        self.assertGreater(res['paused_at'], member['status_at'])

        self.cache_api.update_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid'],
            paused=0)

        res = self.cache_api.get_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid']).__dict__

        self.assertEqual(res['paused'], '0')
        self.assertGreater(res['paused_at'], member['status_at'])

    def test_update_queue_member_only_status(self):
        member = self._create_queue_member()

        self.cache_api.update_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid'], status=3)
        res = self.cache_api.get_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid']).__dict__

        self.assertEqual(res['status'], '3')
        self.assertGreater(res['status_at'], member['status_at'])

    def test__get_members_namespace(self):
        res = self.cache_api._get_members_namespace(
            queue_id='foobar')
        self.assertEqual(res, 'queue:foobar:members')

    def test__get_members_status_namespace(self):
        res = self.cache_api._get_members_status_namespace(
            queue_id='foobar', status=1)
        self.assertEqual(res, 'queue:foobar:members:status:1')

    def test__get_callers_namespace(self):
        res = self.cache_api._get_callers_namespace(
            queue_id='foobar')
        self.assertEqual(res, 'queue:foobar:callers')

    def test__get_callers_status_namespace(self):
        res = self.cache_api._get_callers_status_namespace(
            queue_id='foobar', status=1)
        self.assertEqual(res, 'queue:foobar:callers:status:1')

    def _create_queue_caller(self):
        json = {
            'member_uuid': 'None',
            'name': 'Bob Smith',
            'number': '6135559876',
            'queue_id': '555',
            'status': '1',
        }
        res = self.cache_api.create_queue_caller(
            queue_id=json['queue_id'], name=json['name'],
            number=json['number']).__dict__

        self.assertEqual(len(res), 9)

        for k, v in json.iteritems():
            self.assertEqual(res[k], v)

        # NOTE(pabelanger): We currently check position, we need to test it.
        self.assertTrue(res['created_at'])
        self.assertTrue(res['status_at'])
        self.assertTrue(res['uuid'])

        return res

    def _create_queue_member(self):
        json = {
            'number': '6135551234',
            'paused': '0',
            'queue_id': '555',
            'status': '1',
        }
        res = self.cache_api.create_queue_member(
            queue_id=json['queue_id'], number=json['number']).__dict__

        self.assertEqual(len(res), 8)

        for k, v in json.iteritems():
            self.assertEqual(res[k], v)

        self.assertTrue(res['created_at'])
        self.assertTrue(res['paused_at'])
        self.assertTrue(res['status_at'])
        self.assertTrue(res['uuid'])

        return res
