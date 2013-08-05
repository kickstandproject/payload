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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import redis
import time

from oslo.config import cfg

from stripe.common import exception
from stripe.middleware import models
from stripe.middleware import session as middleware_session
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

get_session = middleware_session.get_session


def get_instance():
    """Return a DB API instance."""
    return Connection()


def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """
    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)

    return query


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
        values['state'] = 'onhold'

        callers = self._get_callers_namespace(queue_id=values['queue_id'])
        self._session.hset(callers, values['uuid'], values['created_at'])

        tmp = '%s:%s' % (callers, values['uuid'])
        self._session.hmset(tmp, values)

        name = self._get_queue_namespace(queue_id=values['queue_id'])
        key = '%s:%s' % (name, values['state'])
        self._session.zadd(key, values['created_at'], values['uuid'])

        return values['uuid']

    def create_queue_member(self, values):
        """Create a new queue member."""
        member = models.QueueMember()
        member.update(values)
        member.save()

        return member

    def delete_queue_member(self, queue_id, id):
        """Delete a queue member."""
        session = get_session()
        with session.begin():
            query = model_query(
                models.QueueMember, session=session
            ).filter_by(queue_id=queue_id, id=id)

            count = query.delete()
            if count != 1:
                raise exception.QueueMemberNotFound(queue_id=queue_id)

            query.delete()

    def get_queue_caller(self, queue_id, uuid):
        """Retrieve information about the given queue caller."""
        callers = self._get_callers_namespace(queue_id=queue_id)
        name = '%s:%s' % (callers, uuid)
        res = self._session.hgetall(name)

        return res

    def get_queue_member(self, queue_id, id):
        """Retrieve information about the given queue member."""
        query = model_query(models.QueueMember).filter_by(
            queue_id=queue_id, id=id)
        result = query.one()

        return result

    def list_queue_callers(self, queue_id, state):
        """Retrieve a list of queue callers."""
        name = self._get_queue_namespace(queue_id=queue_id)
        key = '%s:%s' % (name, state)
        res = self._session.zrange(key, 0, -1)

        if res is None:
            res = []

        return res

    def list_queue_members(self, queue_id):
        """Retrieve a list of queue members."""
        query = model_query(models.QueueMember).filter_by(queue_id=queue_id)

        return [qm for qm in query.all()]

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
