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
from stripe.tests import base
from stripe.tests import utils


class FunctionalTest(base.TestCase):
    def setUp(self):
        super(FunctionalTest, self).setUp()
        self.db_api = db_api.get_instance()

    def _create_test_member(self, **kwargs):
        member = utils.get_test_member(**kwargs)
        self.db_api.create_member(member)
        return member

    def _create_test_queue(self, **kwargs):
        queue = utils.get_test_queue(**kwargs)
        self.db_api.create_queue(queue)
        return queue

    def _create_test_queue_member(self, **kwargs):
        queue_member = utils.get_test_queue_member(**kwargs)
        self.db_api.create_queue_member(queue_member)
        return queue_member
