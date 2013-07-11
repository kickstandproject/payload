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
from stripe import test
from stripe.tests.db import utils


class TestCase(test.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.db_api = db_api.get_instance()

    def test_get_queue_list(self):
        queue = []
        for i in xrange(1, 6):
            q = utils.get_test_queue(id=i)
            self.db_api.create_queue(q)
            queue.append(q['id'])
        res = self.db_api.get_queue_list()
        res.sort()
        queue.sort()
        self.assertEqual(res, queue)
