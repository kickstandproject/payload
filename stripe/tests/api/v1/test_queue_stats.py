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


class TestQueueStatsEmpty(base.FunctionalTest):

    def setUp(self):
        super(TestQueueStatsEmpty, self).setUp()
        self.db_api = db_api.get_instance()
        queue = utils.get_test_queue()
        self.db_api.create_queue(queue)

    def test_empty_get_all(self):
        json = {
            'callers': 0,
            'queue_id': '123',
            'updated_at': None,
        }
        res = self.get_json('/queues/123/stats')
        self.assertEqual(res, json)
