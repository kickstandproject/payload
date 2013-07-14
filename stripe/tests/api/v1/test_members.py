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


class TestMembersEmpty(base.FunctionalTest):

    def test_empty_get_all(self):
        res = self.get_json('/members')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/members/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 500)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        self.db_api = db_api.get_instance()
        for i in xrange(1, 6):
            self._create_test_member(id=i)

    def _create_test_member(self, **kwargs):
        member = utils.get_test_member(**kwargs)
        self.db_api.create_member(member)
        return member

    def test_list_members(self):
        res = self.get_json('/members')
        res.sort()
        self.assertEquals(5, len(res))
        self.assertEquals([1, 2, 3, 4, 5], res)

    def test_delete_member(self):
        self.delete(
            '/members/1', status=200
        )
        res = self.get_json('/members')
        res.sort()
        self.assertEquals(4, len(res))
        self.assertEquals([2, 3, 4, 5], res)

    def test_get_member(self):
        member = self._create_test_member()
        res = self.get_json('/members/%s' % member['id'])
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        self._assertEqualObjects(member, res, ignored_keys)

    def test_create_member(self):
        json = {
            'name': 'Jane Doe',
        }
        res = self.post_json(
            '/members', params=json, status=200
        )
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')

    def test_edit_member(self):
        json = {
            'name': 'renamed',
        }
        res = self.get_json('/members')
        self.assertEquals(len(res), 5)
        member_id = res[0]
        self.put_json(
            '/members/%s' % member_id, params=json
        )
        member = self.db_api.get_member(member_id)
        self.assertEquals(member.name, unicode(json['name']))
