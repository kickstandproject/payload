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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.

from stripe.db import api as db_api
from stripe.tests.api.v1 import base
from stripe.tests.db import utils


class TestQueuesEmpty(base.FunctionalTest):

    def test_empty_get_all(self):
        res = self.get_json('/queues')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/queues/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        self._queues = []
        self.db_api = db_api.get_instance()
        for i in xrange(1, 6):
            q = self._create_test_queue(id=i)
            self._queues.append(q)
        self._queues.sort()

    def _create_test_queue(self, **kwargs):
        queue = utils.get_test_queue(**kwargs)
        self.db_api.create_queue(queue)
        return queue

    def test_list_queues(self):
        res = self.get_json('/queues')
        res.sort()
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        for idx in range(len(res)):
            self._assertEqualObjects(self._queues[idx], res[idx], ignored_keys)

    def test_delete_queue(self):
        self.delete(
            '/queues/1', status=200
        )
        res = self.get_json('/queues')
        res.sort()
        self._queues.pop(0)
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        for idx in range(len(res)):
            self._assertEqualObjects(self._queues[idx], res[idx], ignored_keys)

    def test_get_queue(self):
        queue = self._create_test_queue()
        res = self.get_json('/queues/%s' % queue['id'])
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        self._assertEqualObjects(queue, res, ignored_keys)

    def test_create_queue(self):
        json = {
            'name': 'support',
            'description': 'Support queue',
        }
        res = self.post_json(
            '/queues', params=json, status=200
        )
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')

    def test_edit_queue(self):
        json = {
            'name': 'renamed',
        }
        res = self.get_json('/queues')
        self.assertEquals(len(self._queues), len(res))
        queue_id = res[0]['id']
        self.put_json(
            '/queues/%s' % queue_id, params=json
        )
        queue = self.db_api.get_queue(queue_id)
        self.assertEquals(queue.name, unicode(json['name']))
