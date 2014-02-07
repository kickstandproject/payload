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


def get_api_agent(**kw):
    json = {
        'project_id': kw.get('project_id', 'project1'),
        'user_id': kw.get('user_id', 'user1'),
    }
    return json


def get_api_queue(**kw):
    queue = {
        'description': 'Example queue',
        'disabled': kw.get('disabled', False),
        'name': 'example',
        'uuid': kw.get('uuid', '02d99a62af974b26b510c3564ba84644'),
    }
    return queue


def get_api_queue_caller(**kw):
    caller = {
        'called_id': '6060',
        'caller_id': '5551234',
        'caller_name': 'Bob Jones',
    }
    return caller


def get_api_queue_member(**kw):
    queue_member = {
        'id': kw.get('id', 123),
        'agent_id': kw.get('agent_id', 123),
    }
    return queue_member
