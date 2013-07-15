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


def get_test_member(**kw):
    member = {
        'id': kw.get('id', 123),
        'created_at': None,
        'name': 'John Smith',
        'updated_at': None,
    }
    return member


def get_test_queue(**kw):
    queue = {
        'id': kw.get('id', 123),
        'created_at': None,
        'description': 'Example queue',
        'disabled': kw.get('disabled', False),
        'name': 'example',
        'updated_at': None,
    }
    return queue


def get_test_queue_member(**kw):
    queue_member = {
        'id': kw.get('id', 123),
        'created_at': None,
        'disabled': kw.get('disabled', False),
        'disabled_reason': kw.get('disabled_reason', None),
        'member_id': kw.get('member_id', 123),
        'queue_id': kw.get('queue_id', 123),
        'updated_at': None,
    }
    return queue_member
