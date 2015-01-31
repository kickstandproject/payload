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

from payload.cache import api as cache_api
from payload.cache.api import QueueCallerStatus
from payload.cache.api import QueueMemberStatus
from payload.server import api as server_api
from payload.tests import base


class TestCase(base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.cache_api = cache_api.get_instance()
        self.server_api = server_api.API()

    def test_get_available_queue_caller(self):
        callers = dict()
        for x in range(0, 2):
            callers[x] = self._create_queue_caller()

        res = self.server_api.get_available_queue_caller(
            queue_id=callers[0]['queue_id'])
        self.assertEqual(res, callers[0]['uuid'])

        # Change first callers status so we can return 2nd caller.
        self.cache_api.update_queue_caller(
            queue_id=callers[0]['queue_id'], uuid=callers[0]['uuid'],
            status=QueueCallerStatus.RINGING)
        res = self.server_api.get_available_queue_caller(
            queue_id=callers[0]['queue_id'])
        self.assertEqual(res, callers[1]['uuid'])

        # Get queue caller from queue that does not exist
        res = self.server_api.get_available_queue_caller(
            queue_id='foobar')
        self.assertEqual(res, None)

    def test_get_available_queue_member(self):
        members = dict()
        for x in range(0, 2):
            members[x] = self._create_queue_member()

        res = self.server_api.get_available_queue_member(
            queue_id=members[0]['queue_id'])
        self.assertEqual(res, members[0]['uuid'])

        # Change first members status so we can return 2nd member.
        self.cache_api.update_queue_member(
            queue_id=members[0]['queue_id'], uuid=members[0]['uuid'],
            status=QueueMemberStatus.RINGING)
        res = self.server_api.get_available_queue_member(
            queue_id=members[0]['queue_id'])
        self.assertEqual(res, members[1]['uuid'])

        # Get queue member from queue that does not exist
        res = self.server_api.get_available_queue_member(
            queue_id='foobar')
        self.assertEqual(res, None)

    def _create_queue_caller(self):
        json = {
            'member_uuid': 'None',
            'name': 'Bob Smith',
            'number': '6135559876',
            'queue_id': '555',
            'status': '1',
        }
        res = self.cache_api.create_queue_caller(
            queue_id=json['queue_id'], name=json['name'],
            number=json['number']).__dict__

        self.assertEqual(len(res), 9)

        for k, v in json.iteritems():
            self.assertEqual(res[k], v)

        # NOTE(pabelanger): We currently check position, we need to test it.
        self.assertTrue(res['created_at'])
        self.assertTrue(res['status_at'])
        self.assertTrue(res['uuid'])

        return res

    def _create_queue_member(self):
        json = {
            'number': '6135551234',
            'paused': '0',
            'queue_id': '555',
            'status': '1',
        }
        res = self.cache_api.create_queue_member(
            queue_id=json['queue_id'], number=json['number']).__dict__

        self.assertEqual(len(res), 8)

        for k, v in json.iteritems():
            self.assertEqual(res[k], v)

        self.assertTrue(res['created_at'])
        self.assertTrue(res['paused_at'])
        self.assertTrue(res['status_at'])
        self.assertTrue(res['uuid'])

        return res
