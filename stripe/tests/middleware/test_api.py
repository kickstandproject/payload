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

from stripe.tests.middleware import base


class TestCase(base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()

    def test_create_queue_caller(self):
        self._create_queue_caller(queue_id=1)

    def test_delete_queue_caller(self):
        callers = self._create_queue_caller(queue_id=1)

        self.middleware_api.delete_queue_caller(
            id=callers[0]['id'],
            queue_id=callers[0]['queue_id'],
        )

        callers.pop(0)
        self._list_queue_callers(callers)

    def test_list_queue_callers(self):
        callers = self._create_queue_caller(queue_id=1)
        self._list_queue_callers(callers)

    def _list_queue_callers(self, callers):
        res = self.middleware_api.list_queue_callers(
            callers[0]['queue_id']
        )
        self.assertEqual(len(res), len(callers))

        for idx in range(len(res)):
            self._validate_queue_caller(
                original=callers[idx], result=res[idx]
            )

    def test_get_queue_callers(self):
        callers = self._create_queue_caller(queue_id=1)
        res = self.middleware_api.get_queue_caller(
            id=callers[0]['id'],
            queue_id=callers[0]['queue_id'],
        )
        self._validate_queue_caller(
            original=callers[0], result=res
        )
