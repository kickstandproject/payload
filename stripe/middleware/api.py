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

from stripe.common import exception
from stripe.middleware import models
from stripe.middleware import session as middleware_session

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

    def create_queue_caller(self, data):
        caller = models.QueueCaller()
        caller.update(data)
        caller.save()

        return caller

    def delete_queue_caller(self, queue_id, id):
        """Delete a queue caller."""
        session = get_session()
        with session.begin():
            query = model_query(
                models.QueueCaller, session=session
            ).filter_by(queue_id=queue_id, id=id)

            count = query.delete()
            if count != 1:
                raise exception.QueueCallerNotFound(queue_id=queue_id)

            query.delete()

    def get_queue_caller(self, queue_id, id):
        """Retrieve information about the given queue caller."""
        query = model_query(models.QueueCaller).filter_by(
            queue_id=queue_id, id=id)
        result = query.one()

        return result

    def list_queue_callers(self, queue_id):
        """Retrieve a list of queue callers."""
        query = model_query(models.QueueCaller).filter_by(queue_id=queue_id)

        return [qc for qc in query.all()]

    def get_queue_stats(self, id):
        # TODO(pabelanger): Implement redis backend for queue callers.
        res = {
            'callers': 0,
            'queue_id': id,
            'updated_at': None,
        }

        return res
