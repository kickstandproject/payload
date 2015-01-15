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

import time

from payload.cache import api
from payload.common import exception
from payload import messaging
from payload.tests import base


class TestCase(base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        messaging.setup('fake://')
        self.addCleanup(messaging.cleanup)
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

    def test_update_queue_caller(self):
        caller = self._create_queue_caller()
        time.sleep(1)

        self.cache_api.update_queue_caller(
            queue_id=caller['queue_id'], uuid=caller['uuid'],
            member_uuid='9876', name='Jim', number='1234', status=3)

        res = self.cache_api.get_queue_caller(
            queue_id=caller['queue_id'], uuid=caller['uuid']).__dict__

        self.assertEqual(res['name'], 'Jim')
        self.assertEqual(res['number'], '1234')
        self.assertEqual(res['status'], '3')
        self.assertEqual(res['member_uuid'], '9876')
        self.assertNotEqual(caller['status_at'], res['status_at'])

    def test_update_queue_member(self):
        member = self._create_queue_member()
        time.sleep(1)

        self.cache_api.update_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid'],
            number='1234', paused=True, status=3)

        res = self.cache_api.get_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid']).__dict__

        self.assertEqual(res['number'], '1234')
        self.assertEqual(res['paused'], 'True')
        self.assertEqual(res['status'], '3')
        self.assertNotEqual(member['status_at'], res['status_at'])

    def _create_queue_caller(self):
        json = {
            'member_uuid': 'None',
            'name': 'Bob Smith',
            'number': '6135559876',
            'position': 0,
            'queue_id': '555',
            'status': '0',
        }
        res = self.cache_api.create_queue_caller(
            queue_id=json['queue_id'], name=json['name'],
            number=json['number']).__dict__

        self.assertEqual(len(res), 9)

        for k, v in json.iteritems():
            self.assertEqual(res[k], v)

        self.assertTrue(res['created_at'])
        self.assertTrue(res['status_at'])
        self.assertTrue(res['uuid'])

        return res

    def _create_queue_member(self):
        json = {
            'number': '6135551234',
            'paused': 'False',
            'queue_id': '555',
            'status': '0',
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
