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
        member = utils.get_test_member()
        self.db_api.create_member(member)
        queue = utils.get_test_queue()
        self.db_api.create_queue(queue)

    def _create_test_queue_member(self, **kwargs):
        queue_member = utils.get_test_queue_member(**kwargs)
        self.db_api.create_queue_member(queue_member)
        return queue_member

    def test_create_queue_member(self):
        self._create_test_queue_member()

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
        queue_id = 1
        queue = utils.get_test_queue(id=queue_id)
        self.db_api.create_queue(queue)

        for i in xrange(1, 6):
            qm = self._create_test_queue_member(id=i)
            queue_member.append(qm['id'])
        for i in xrange(7, 8):
            qm = self._create_test_queue_member(id=i, queue_id=queue_id)
            queue_member.append(qm['id'])
        res = self.db_api.get_queue_member_list()
        res.sort()
        queue_member.sort()
        self.assertEqual(len(res), len(queue_member))

    def test_get_queue_member_list_by_queue_id(self):
        queue_member = []
        queue_id = 1
        queue = utils.get_test_queue(id=queue_id)
        self.db_api.create_queue(queue)

        for i in xrange(1, 6):
            self._create_test_queue_member(id=i)

        for i in xrange(7, 8):
            qm = self._create_test_queue_member(id=i, queue_id=queue_id)
            queue_member.append(qm['id'])

        res = self.db_api.get_queue_member_list(queue_id=queue_id)
        res.sort()
        queue_member.sort()
        self.assertEqual(len(res), len(queue_member))
