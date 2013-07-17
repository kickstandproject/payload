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
from stripe.tests.db import base


class TestCase(base.FunctionalTest):

    def test_create_member(self):
        self._create_test_member()

    def test_delete_member(self):
        member = self._create_test_member()
        self.db_api.delete_member(member['id'])
        self.assertRaises(
            exception.MemberNotFound, self.db_api.get_member, member['id']
        )

    def test_delete_member_not_found(self):
        self.assertRaises(
            exception.MemberNotFound, self.db_api.delete_member, 123
        )

    def test_get_member_by_id(self):
        member = self._create_test_member()
        res = self.db_api.get_member(member['id'])
        self.assertEqual(member['id'], res['id'])

    def test_get_member_list(self):
        member = []
        for i in xrange(1, 6):
            q = self._create_test_member(id=i)
            member.append(q)
        res = self.db_api.get_member_list()
        res.sort()
        member.sort()
        self.assertEqual(len(res), len(member))
