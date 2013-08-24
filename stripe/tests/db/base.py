# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from stripe.db import api as db_api
from stripe.tests import base
from stripe.tests.db import utils


class FunctionalTest(base.TestCase):
    def setUp(self):
        super(FunctionalTest, self).setUp()
        self.db_api = db_api.get_instance()

    def _create_test_agent(self, **kwargs):
        agent = utils.get_db_agent(**kwargs)
        self.db_api.create_agent(agent)
        return agent

    def _create_test_queue(self, **kwargs):
        queue = utils.get_db_queue(**kwargs)
        self.db_api.create_queue(queue)
        return queue

    def _create_test_queue_member(self, **kwargs):
        queue_member = utils.get_db_queue_member(**kwargs)
        self.db_api.create_queue_member(queue_member)
        return queue_member
