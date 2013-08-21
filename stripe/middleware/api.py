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

import redis
import time

from oslo.config import cfg

from stripe.openstack.common import uuidutils

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
CONF.register_opts(redis_opts, 'middleware')


def get_instance():
    """Return a DB API instance."""
    return Connection()


class QueueCallerStatus(object):

    ONHOLD, RINGING, ONCALL, HUNGUP = range(1, 5)


class Connection(object):

    _session = None
    _queue_namespace = 'queue'

    def __init__(self):
        self._session = redis.StrictRedis(
            host=CONF.middleware.host, port=CONF.middleware.port,
            db=CONF.middleware.database, password=CONF.middleware.password,
        )

    def create_queue_caller(self, values):
        values['created_at'] = time.time()
        values['uuid'] = uuidutils.generate_uuid()
        status = QueueCallerStatus.ONHOLD

        callers = self._get_callers_namespace(queue_id=values['queue_id'])
        self._session.hset(callers, values['uuid'], values['created_at'])

        tmp = '%s:%s' % (callers, values['uuid'])
        self._session.hmset(tmp, values)

        self._create_queue_caller_status(
            queue_id=values['queue_id'], status=status,
            timestamp=values['created_at'], uuid=values['uuid'],
        )

        res = self.get_queue_caller(
            queue_id=values['queue_id'], uuid=values['uuid']
        )

        return res

    def _queue_caller_status(self, queue_id, status, uuid):
        name = self._get_queue_namespace(queue_id=queue_id)
        key = '%s:%s' % (name, status)

        return key

    def _create_queue_caller_status(self, queue_id, status, timestamp, uuid):
        key = self._queue_caller_status(
            queue_id=queue_id, status=status, uuid=uuid
        )
        self._session.zadd(key, timestamp, uuid)
        callers = self._get_callers_namespace(queue_id=queue_id)
        tmp = '%s:%s' % (callers, uuid)
        self._session.hset(tmp, 'status', status)

    def _delete_queue_caller_status(self, queue_id, status, uuid):
        key = self._queue_caller_status(
            queue_id=queue_id, status=status, uuid=uuid
        )
        self._session.zrem(key, uuid)

    def get_queue_caller(self, queue_id, uuid):
        """Retrieve information about the given queue caller."""
        callers = self._get_callers_namespace(queue_id=queue_id)
        name = '%s:%s' % (callers, uuid)
        res = self._session.hgetall(name)

        return res

    def list_queue_callers(self, queue_id, status=None):
        """Retrieve a list of queue callers."""
        if status is None:
            status = QueueCallerStatus.ONHOLD

        name = self._get_queue_namespace(queue_id=queue_id)
        key = '%s:%s' % (name, status)
        data = self._session.zrange(key, 0, -1)
        res = []
        for uuid in data:
            res.append(self.get_queue_caller(
                queue_id=queue_id, uuid=uuid
            ))

        return res

    def set_queue_caller_status(self, queue_id, status, uuid):
        res = self.get_queue_caller(queue_id=queue_id, uuid=uuid)

        # Delete caller from current sorted set
        self._delete_queue_caller_status(
            queue_id=queue_id, status=res['status'], uuid=uuid
        )

        # Add caller to new sorted set
        self._create_queue_caller_status(
            queue_id=queue_id, status=status, timestamp=time.time(), uuid=uuid
        )

    def get_queue_stats(self, id):
        # TODO(pabelanger): Implement redis backend for queue callers.
        res = {
            'callers': 0,
            'queue_id': id,
            'updated_at': None,
        }

        return res

    def _get_queue_namespace(self, queue_id):
        name = '%s:%s' % (self._queue_namespace, queue_id)

        return name

    def _get_callers_namespace(self, queue_id):
        name = self._get_queue_namespace(queue_id=queue_id)
        callers = '%s:%s' % (name, 'callers')

        return callers
