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


def get_middleware_agent(**kw):
    agent = {
        'id': kw.get('id', 123),
        'name': 'John Smith',
    }
    return agent


def get_middleware_queue(**kw):
    queue = {
        'id': kw.get('id', 123),
        'description': 'Example queue',
        'disabled': kw.get('disabled', False),
        'name': 'example',
    }
    return queue


def get_middleware_queue_caller(**kw):
    json = {
        'uuid': '3649acc0411a11e3aa6e0800200c9a66'}

    return json


def get_middleware_queue_member(**kw):
    queue_member = {
        'extension': kw.get('extension', 'alice@example.org'),
    }
    return queue_member
