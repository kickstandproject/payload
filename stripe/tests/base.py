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

from stripe import test
from stripe.tests import utils


class TestCase(test.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()

    def _validate_queue_caller(self, original, result):
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        self._assertEqualObjects(original, result, ignored_keys)

    def _create_queue_caller(self, session, **kwargs):
        callers = []
        for i in xrange(1, 6):
            kwargs['id'] = i
            caller = utils.get_test_queue_caller(**kwargs)
            session.create_queue_caller(caller)
            callers.append(caller)

        self.assertEqual(len(callers), 5)

        return callers
