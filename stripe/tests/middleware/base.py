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

from stripe.middleware import api as middleware_api
from stripe.tests import base
from stripe.tests.middleware import utils


class TestCase(base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.middleware_api = middleware_api.get_instance()

    def _create_queue_caller(self, queue_id, **kwargs):
        callers = []
        caller = utils.get_middleware_queue_caller(**kwargs)
        res = self.middleware_api.create_queue_caller(
            queue_id=queue_id, values=caller
        )
        callers.append(res)

        return callers

    def _create_queue_member(self, agent_id, queue_id, **kwargs):
        members = []
        member = utils.get_middleware_queue_member(**kwargs)
        res = self.middleware_api.create_queue_member(
            agent_id=agent_id, queue_id=queue_id, values=member
        )
        members.append(res)

        return members
