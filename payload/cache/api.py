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

from payload.cache import models
from payload.common import exception
from payload import messaging
from payload.openstack.common import context
from payload.openstack.common import log as logging
from payload.openstack.common import timeutils
from payload.openstack.common import uuidutils

LOG = logging.getLogger(__name__)

cache_opts = [
    cfg.StrOpt(
        'host', default='127.0.0.1', help='Hostname'),
    cfg.IntOpt(
        'port', default=6379, help='The specific TCP port Redis listens on'),
    cfg.IntOpt(
        'database', default=0, help='Which Redis database to use'),
    cfg.StrOpt(
        'password', default=None, help='Password to use with AUTH command'),
]

CONF = cfg.CONF
CONF.register_opts(cache_opts, 'redis')


def get_instance():
    """Return a Redis API instance."""
    return Connection()


def _send_notification(event, payload):
    notification = event.replace(" ", "_")
    notification = "queue.%s" % notification
    notifier = messaging.get_notifier('payload')
    notifier.info(context.RequestContext(), notification, payload)


class Connection(object):

    _session = None
    _queue_namespace = 'queue'

    def __init__(self):
        self._session = redis.StrictRedis(
            host=CONF.redis.host, port=CONF.redis.port,
            db=CONF.redis.database, password=CONF.redis.password)

    def create_queue_caller(
            self, queue_id, uuid=None, member_uuid=None, name=None,
            number=None, status=0):
        timestamp = timeutils.utcnow_ts()
        values = {
            'created_at': timeutils.iso8601_from_timestamp(timestamp),
            'member_uuid': member_uuid,
            'name': name,
            'number': number,
            'queue_id': queue_id,
            'status': status,
            'status_at': timeutils.iso8601_from_timestamp(timestamp),
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

        _send_notification('caller.create', res.__dict__)

        return res

    def create_queue_member(
            self, queue_id, number, uuid=None, paused=False, status=0):
        timestamp = timeutils.utcnow_ts()
        values = {
            'created_at': timeutils.iso8601_from_timestamp(timestamp),
            'number': number,
            'paused': paused,
            'paused_at': timeutils.iso8601_from_timestamp(timestamp),
            'queue_id': queue_id,
            'status': status,
            'status_at': timeutils.iso8601_from_timestamp(timestamp),
        }
        if uuid:
            values['uuid'] = uuid
        else:
            values['uuid'] = uuidutils.generate_uuid()

        key = self._get_members_namespace(queue_id=queue_id)
        self._session.zadd(key, timestamp, values['uuid'])

        member = '%s:%s' % (key, values['uuid'])
        self._session.hmset(member, values)

        res = self.get_queue_member(
            queue_id=queue_id, uuid=values['uuid'])

        _send_notification('member.create', res.__dict__)

        return res

    def delete_queue_caller(self, queue_id, uuid):
        res = self.get_queue_caller(
            queue_id=queue_id, uuid=uuid)
        _send_notification('caller.delete', res.__dict__)

        key = self._get_callers_namespace(queue_id=queue_id)
        self._session.zrem(key, uuid)
        caller = '%s:%s' % (key, uuid)
        self._session.delete(caller)

    def delete_queue_member(self, queue_id, uuid):
        res = self.get_queue_member(
            queue_id=queue_id, uuid=uuid)
        _send_notification('member.delete', res.__dict__)

        key = self._get_members_namespace(queue_id=queue_id)
        self._session.zrem(key, uuid)
        member = '%s:%s' % (key, uuid)
        self._session.delete(member)

    def get_queue_caller(self, queue_id, uuid):
        """Retrieve information about the given queue caller."""
        key = '%s:%s' % (self._get_callers_namespace(queue_id=queue_id), uuid)
        res = self._session.hgetall(key)

        if not any(res):
            raise exception.QueueCallerNotFound(uuid=uuid)

        key = self._get_callers_namespace(queue_id=queue_id)
        res['position'] = self._session.zrank(key, uuid)

        caller = models.QueueCaller(
            uuid=res['uuid'], created_at=res['created_at'],
            member_uuid=res['member_uuid'], name=res['name'],
            number=res['number'], position=res['position'],
            queue_id=res['queue_id'], status=res['status'],
            status_at=res['status_at'])

        return caller

    def get_queue_member(self, queue_id, uuid):
        """Retrieve information about the given queue member."""
        key = '%s:%s' % (self._get_members_namespace(queue_id=queue_id), uuid)
        res = self._session.hgetall(key)

        if not any(res):
            raise exception.QueueMemberNotFound(uuid=uuid)

        caller = models.QueueMember(
            uuid=res['uuid'], created_at=res['created_at'],
            number=res['number'], paused=res['paused'],
            paused_at=res['paused_at'], queue_id=res['queue_id'],
            status=res['status'], status_at=res['status_at'])

        return caller

    def list_queue_callers(self, queue_id):
        """Retrieve a list of queue callers."""
        data = self._list_queue_callers(queue_id=queue_id)

        res = []
        for uuid in data:
            res.append(self.get_queue_caller(
                queue_id=queue_id, uuid=uuid))

        return res

    def list_queue_members(self, queue_id):
        """Retrieve a list of queue members."""
        data = self._list_queue_members(queue_id=queue_id)

        res = []
        for uuid in data:
            res.append(self.get_queue_member(
                queue_id=queue_id, uuid=uuid))

        return res

    def update_queue_caller(
            self, queue_id, uuid, member_uuid=None, name=None, number=None,
            status=None):
        timestamp = timeutils.utcnow_ts()
        key = self._get_callers_namespace(queue_id=queue_id)
        caller = '%s:%s' % (key, uuid)
        data = dict()

        if member_uuid is not None:
            data['member_uuid'] = member_uuid
        if name is not None:
            data['name'] = name
        if number is not None:
            data['number'] = number
        if status is not None:
            data['status'] = status
            data['status_at'] = timeutils.iso8601_from_timestamp(timestamp)

        self._session.hmset(caller, data)

        res = self.get_queue_caller(
            queue_id=queue_id, uuid=uuid)

        _send_notification('caller.update', res.__dict__)

    def update_queue_member(
            self, queue_id, uuid, number=None, paused=None, status=None):
        timestamp = timeutils.utcnow_ts()
        key = self._get_members_namespace(queue_id=queue_id)
        member = '%s:%s' % (key, uuid)
        data = dict()

        if number is not None:
            data['number'] = number
        if paused is not None:
            data['paused'] = paused
            data['paused_at'] = timeutils.iso8601_from_timestamp(timestamp)
        if status is not None:
            data['status'] = status
            data['status_at'] = timeutils.iso8601_from_timestamp(timestamp)

        self._session.hmset(member, data)

        res = self.get_queue_member(
            queue_id=queue_id, uuid=uuid)

        _send_notification('member.update', res.__dict__)

    def _list_queue_callers(self, queue_id):
        key = self._get_callers_namespace(queue_id=queue_id)

        return self._session.zrange(key, 0, -1)

    def _list_queue_members(self, queue_id):
        key = self._get_members_namespace(queue_id=queue_id)

        return self._session.zrange(key, 0, -1)

    def _get_queue_namespace(self, queue_id):
        name = '%s:%s' % (self._queue_namespace, queue_id)

        return name

    def _get_callers_namespace(self, queue_id):
        name = self._get_queue_namespace(queue_id=queue_id)
        key = '%s:%s' % (name, 'callers')

        return key

    def _get_members_namespace(self, queue_id):
        name = self._get_queue_namespace(queue_id=queue_id)
        key = '%s:%s' % (name, 'members')

        return key
