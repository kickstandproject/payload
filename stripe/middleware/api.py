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


class QueueMemberStatus(object):

    WAITING, ONCALL = range(1, 3)


class Connection(object):

    _session = None
    _queue_namespace = 'queue'

    def __init__(self):
        self._session = redis.StrictRedis(
            host=CONF.middleware.host, port=CONF.middleware.port,
            db=CONF.middleware.database, password=CONF.middleware.password,
        )

    def create_queue_caller(self, queue_id, values):
        values['created_at'] = time.time()
        values['uuid'] = uuidutils.generate_uuid()
        status = QueueCallerStatus.ONHOLD

        callers = self._get_callers_namespace(queue_id=queue_id)
        self._session.hset(callers, values['uuid'], values['created_at'])

        tmp = '%s:%s' % (callers, values['uuid'])
        self._session.hmset(tmp, values)

        self._create_queue_caller_status(
            queue_id=queue_id, status=status, timestamp=values['created_at'],
            uuid=values['uuid'],
        )

        res = self.get_queue_caller(
            queue_id=queue_id, uuid=values['uuid']
        )

        return res

    def create_queue_member(self, agent_id, queue_id, values):
        values['created_at'] = time.time()
        status = QueueMemberStatus.WAITING

        members = self._get_members_namespace(queue_id=queue_id)
        self._session.hset(members, agent_id, values['created_at'])

        tmp = '%s:%s' % (members, agent_id)
        self._session.hmset(tmp, values)

        self._create_queue_member_status(
            agent_id=agent_id, queue_id=queue_id, status=status,
            timestamp=values['created_at'],
        )

        res = self.get_queue_member(agent_id=agent_id, queue_id=queue_id)

        return res

    def delete_queue_caller(self, queue_id, uuid):
        self._set_queue_caller_status(
            queue_id=queue_id, status=QueueCallerStatus.HUNGUP, uuid=uuid
        )

    def _queue_caller_status(self, queue_id, status):
        name = self._get_queue_namespace(queue_id=queue_id)
        key = '%s:%s' % (name, status)

        return key

    def _queue_member_status(self, queue_id, status):
        name = self._get_queue_namespace(queue_id=queue_id)
        key = '%s:%s' % (name, status)

        return key

    def _create_queue_caller_status(self, queue_id, status, timestamp, uuid):
        key = self._queue_caller_status(
            queue_id=queue_id, status=status
        )
        self._session.zadd(key, timestamp, uuid)
        callers = self._get_callers_namespace(queue_id=queue_id)
        tmp = '%s:%s' % (callers, uuid)
        self._session.hset(tmp, 'status', status)

    def _create_queue_member_status(
            self, agent_id, queue_id, status, timestamp):
        key = self._queue_member_status(
            queue_id=queue_id, status=status
        )
        self._session.zadd(key, timestamp, agent_id)
        members = self._get_members_namespace(queue_id=queue_id)
        tmp = '%s:%s' % (members, agent_id)
        self._session.hset(tmp, 'status', status)

    def _delete_queue_caller_status(self, queue_id, status, uuid):
        key = self._queue_caller_status(
            queue_id=queue_id, status=status
        )
        self._session.zrem(key, uuid)

    def get_queue_caller(self, queue_id, uuid):
        """Retrieve information about the given queue caller."""
        callers = self._get_callers_namespace(queue_id=queue_id)
        name = '%s:%s' % (callers, uuid)
        res = self._session.hgetall(name)

        try:
            name = self._get_queue_namespace(queue_id=queue_id)
            key = '%s:%s' % (name, res['status'])
            res['position'] = self._session.zrank(key, uuid)
        except Exception:
            pass

        return res

    def get_queue_member(self, agent_id, queue_id):
        """Retrieve information about the given queue member."""
        members = self._get_members_namespace(queue_id=queue_id)
        name = '%s:%s' % (members, agent_id)
        res = self._session.hgetall(name)

        return res

    def list_queue_callers(self, queue_id, status=None):
        """Retrieve a list of queue callers."""
        if status is None:
            status = QueueCallerStatus.ONHOLD

        data = self._list_queue_callers(queue_id=queue_id, status=status)

        res = []
        for uuid in data:
            res.append(self.get_queue_caller(
                queue_id=queue_id, uuid=uuid
            ))

        return res

    def list_queue_members(self, queue_id, status=None):
        """Retrieve a list of queue members."""
        if status is None:
            status = QueueMemberStatus.WAITING

        data = self._list_queue_members(queue_id=queue_id, status=status)

        res = []
        for agent_id in data:
            res.append(self.get_queue_member(
                agent_id, queue_id=queue_id,
            ))

        return res

    def _count_queue_callers(self, queue_id, status):
        key = self._queue_caller_status(
            queue_id=queue_id, status=status
        )

        return self._session.zcard(key)

    def _list_queue_callers(self, queue_id, status):
        key = self._queue_caller_status(
            queue_id=queue_id, status=status
        )

        return self._session.zrange(key, 0, -1)

    def _list_queue_members(self, queue_id, status):
        key = self._queue_member_status(
            queue_id=queue_id, status=status
        )

        return self._session.zrange(key, 0, -1)

    def _set_queue_caller_status(self, queue_id, status, uuid):
        res = self.get_queue_caller(queue_id=queue_id, uuid=uuid)

        # Delete caller from current sorted set
        self._delete_queue_caller_status(
            queue_id=queue_id, status=res['status'], uuid=uuid
        )

        # Add caller to new sorted set
        self._create_queue_caller_status(
            queue_id=queue_id, status=status, timestamp=time.time(), uuid=uuid
        )

    def get_queue_stats(self, queue_id, status=None):
        """Retrieve stats for a queue."""
        if status is None:
            status = QueueCallerStatus.ONHOLD

        callers = self._count_queue_callers(queue_id=queue_id, status=status)

        res = {
            'callers': callers,
        }

        return res

    def _get_queue_namespace(self, queue_id):
        name = '%s:%s' % (self._queue_namespace, queue_id)

        return name

    def _get_callers_namespace(self, queue_id):
        name = self._get_queue_namespace(queue_id=queue_id)
        callers = '%s:%s' % (name, 'callers')

        return callers

    def _get_members_namespace(self, queue_id):
        name = self._get_queue_namespace(queue_id=queue_id)
        members = '%s:%s' % (name, 'members')

        return members
