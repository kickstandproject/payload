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

from stripe.common import exception
from stripe.db import api as db_api
from stripe import test
from stripe.tests.db import utils


class TestCase(test.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.db_api = db_api.get_instance()

    def _create_test_queue(self, **kwargs):
        queue = utils.get_test_queue(**kwargs)
        self.db_api.create_queue(queue)
        return queue

    def test_create_queue(self):
        self._create_test_queue()

    def test_delete_queue(self):
        queue = self._create_test_queue()
        self.db_api.delete_queue(queue['id'])
        self.assertRaises(
            exception.QueueNotFound, self.db_api.get_queue, queue['id']
        )

    def test_delete_queue_not_found(self):
        self.assertRaises(
            exception.QueueNotFound, self.db_api.delete_queue, 123
        )

    def test_get_queue_by_id(self):
        queue = self._create_test_queue()
        res = self.db_api.get_queue(queue['id'])
        self.assertEqual(queue['id'], res['id'])

    def test_get_queue_list(self):
        queue = []
        for i in xrange(1, 6):
            q = self._create_test_queue(id=i)
            queue.append(q)
        res = self.db_api.get_queue_list()
        res.sort()
        queue.sort()
        self.assertEqual(len(res), len(queue))
