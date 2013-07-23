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

import redis

from oslo.config import cfg

redis_opts = [
    cfg.StrOpt('host',
               default='127.0.0.1',
               help='Host to locate redis'),
    cfg.IntOpt('port',
               default=6379,
               help='Use this port to connect to redis host.'),
    cfg.StrOpt('password',
               default=None,
               help='Password for Redis server. (optional)'),
]

CONF = cfg.CONF
CONF.register_opts(redis_opts, 'redis')


def get_instance():
    """Return a DB API instance."""
    return Connection()


class Connection(object):
    _redis = None

    def __init__(self):
        self._redis = redis.StrictRedis(
            host=CONF.redis.host, password=CONF.redis.password,
            port=CONF.redis.port,
        )

    def get_queue_callers(self, id):
        # TODO(pabelanger): Implement redis backend for queue callers.
        res = {
            'id': 1,
            'created_at': None,
            'name': 'John Doe',
            'number': '6135551234',
            'position': 1,
            'queue_id': id,
            'updated_at': None,
        }

        return res

    def get_queue_stats(self, id):
        # TODO(pabelanger): Implement redis backend for queue callers.
        callers = self._redis.llen(id)
        res = {
            'callers': callers,
            'queue_id': id,
            'updated_at': None,
        }

        return res
