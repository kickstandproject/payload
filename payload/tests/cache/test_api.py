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
from payload import messaging
from payload.tests import base


class TestCase(base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        messaging.setup('fake://')
        self.addCleanup(messaging.cleanup)
        self.cache_api = api.get_instance()

    def test_create_queue_caller(self):
        json = {
            'name': 'None',
            'number': 'None',
            'position': 0,
            'queue_id': '555',
            'status': '0',
        }
        res = self._create_queue_caller(
            queue_id=json['queue_id'])

        self.assertEqual(len(res), 8)

        for k, v in json.iteritems():
            self.assertEqual(res[k], v)

        self.assertTrue(res['created_at'])
        self.assertTrue(res['status_at'])
        self.assertTrue(res['uuid'])

    def test_create_queue_member(self):
        json = {
            'number': '6135551234',
            'paused': 'False',
            'queue_id': '555',
            'status': '0',
        }
        res = self._create_queue_member(
            queue_id=json['queue_id'], number=json['number'])

        self.assertEqual(len(res), 8)

        for k, v in json.iteritems():
            self.assertEqual(res[k], v)

        self.assertTrue(res['created_at'])
        self.assertTrue(res['paused_at'])
        self.assertTrue(res['status_at'])
        self.assertTrue(res['uuid'])

    def test_delete_queue_caller(self):
        caller = self._create_queue_caller(queue_id='12345')
        self.assertTrue(caller['queue_id'])
        self.assertTrue(caller['uuid'])

        self.cache_api.delete_queue_caller(
            queue_id=caller['queue_id'], uuid=caller['uuid'])

        self.assertRaises(
            exception.QueueCallerNotFound,
            self.cache_api.get_queue_caller,
            queue_id=caller['queue_id'], uuid=caller['uuid'])

    def test_delete_queue_member(self):
        member = self._create_queue_member(queue_id='12345', number='test')
        self.assertTrue(member['queue_id'])
        self.assertTrue(member['uuid'])

        self.cache_api.delete_queue_member(
            queue_id=member['queue_id'], uuid=member['uuid'])

        self.assertRaises(
            exception.QueueMemberNotFound,
            self.cache_api.get_queue_member,
            queue_id=member['queue_id'], uuid=member['uuid'])

    def _create_queue_caller(self, queue_id, **kwargs):
        res = self.cache_api.create_queue_caller(
            queue_id=queue_id, **kwargs)

        return res.__dict__

    def _create_queue_member(self, queue_id, number, **kwargs):
        res = self.cache_api.create_queue_member(
            queue_id=queue_id, number=number, **kwargs)

        return res.__dict__
