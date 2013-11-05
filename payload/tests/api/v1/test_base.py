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

from payload.tests.api.v1 import base


class TestCase(base.FunctionalTest):

    def test_404_not_found(self):
        response = self.get_json(
            '/foo', expect_errors=True, headers={'Accept': 'application/json'}
        )
        self.assertEqual(response.status_int, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertTrue(response.json['error_message'])
