# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013-2014 PolyBeacon, Inc.
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

import redis

from oslo.config import cfg

from payload.openstack.common import log as logging
from payload.openstack.common import timeutils
from payload.openstack.common import uuidutils
from payload.redis import models

LOG = logging.getLogger(__name__)

redis_opts = [
    cfg.StrOpt(
        'host', default='127.0.0.1', help='Hostname',
    ),
    cfg.IntOpt(
        'port', default=6379, help='The specific TCP port Redis listens on',
    ),
    cfg.IntOpt(
        'database', default=0, help='Which Redis database to use',
    ),
    cfg.StrOpt(
        'password', default=None, help='Password to use with AUTH command',
    ),
]

CONF = cfg.CONF
CONF.register_opts(redis_opts, 'redis')


def get_instance():
    """Return a Redis API instance."""
    return Connection()


class Connection(object):

    _session = None
    _queue_namespace = 'queue'

    def __init__(self):
        self._session = redis.StrictRedis(
            host=CONF.redis.host, port=CONF.redis.port,
            db=CONF.redis.database, password=CONF.redis.password)

    def create_queue_caller(self, queue_id, uuid=None, name=None, number=None):
        timestamp = timeutils.utcnow_ts()
        values = {
            'created_at': timeutils.iso8601_from_timestamp(timestamp),
            'name': name,
            'number': number,
        }
        if uuid:
            values['uuid'] = uuid
        else:
            values['uuid'] = uuidutils.generate_uuid()

        key = self._get_callers_namespace(queue_id=queue_id)
        self._session.zadd(key, timestamp, values['uuid'])

        caller = '%s:%s' % (key, values['uuid'])
        self._session.hmset(caller, values)

        res = self.get_queue_caller(
            queue_id=queue_id, uuid=values['uuid'])

        return res

    def delete_queue_caller(self, queue_id, uuid):
        key = self._get_callers_namespace(queue_id=queue_id)
        self._session.zrem(key, uuid)
        caller = '%s:%s' % (key, uuid)
        self._session.delete(caller)

    def get_queue_caller(self, queue_id, uuid):
        """Retrieve information about the given queue caller."""
        key = '%s:%s' % (self._get_callers_namespace(queue_id=queue_id), uuid)
        res = self._session.hgetall(key)

        key = self._get_callers_namespace(queue_id=queue_id)
        res['position'] = self._session.zrank(key, uuid)

        caller = models.QueueCaller(
            uuid=res['uuid'], created_at=res['created_at'], name=res['name'],
            number=res['number'], position=res['position'])

        return caller

    def list_queue_callers(self, queue_id):
        """Retrieve a list of queue callers."""
        data = self._list_queue_callers(queue_id=queue_id)

        res = []
        for uuid in data:
            res.append(self.get_queue_caller(
                queue_id=queue_id, uuid=uuid))

        return res

    def _list_queue_callers(self, queue_id):
        key = self._get_callers_namespace(queue_id=queue_id)

        return self._session.zrange(key, 0, -1)

    def _get_queue_namespace(self, queue_id):
        name = '%s:%s' % (self._queue_namespace, queue_id)

        return name

    def _get_callers_namespace(self, queue_id):
        name = self._get_queue_namespace(queue_id=queue_id)
        callers = '%s:%s' % (name, 'callers')

        return callers
